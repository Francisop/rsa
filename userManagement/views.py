from django.http import Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.db.models.functions import Substr
from django.db.models import Max
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes
import os

from schoolManagement.models import SchoolClass, SchoolSession

User = get_user_model()


def check_matric():
    latest_user = User.objects.annotate(
        year=Substr('matric', 4, 2),
        number=Substr('matric', 7, 2),
    ).aggregate(
        latest_number=Max('number')
    )
    print(latest_user)
    if latest_user['latest_number'] != None:

        latest_matric = latest_user['latest_number']

        # latest_user = User.objects.get(matric=latest_matric)
        print(latest_matric)
        return latest_matric
    else:
        return None


def gen_matric():
    num = check_matric()
    now = datetime.now()
    year_str = now.strftime("%y")
    if num != None:
        num = int(num) + 1
        matric = "RSA{}_{}".format(year_str, num)
        return matric
    else:
        matric = "RSA{}_{}".format(year_str, 1)
        return matric


class Register(APIView):

    def post(self, request, format=None):
        # print(request.data)

        user_data = request.data
        print(gen_matric())
        # print(request.data)
        if user_data['role'] == 'student':

            # class ref
            class_ref = SchoolClass.objects.get(pk=request.data['school_class'])
            request.data['school_class'] = class_ref.pk
            class_ref.number_of_students = class_ref.number_of_students + 1
            class_ref.save()
            # sesion ref
            # sess_ref = SchoolSession.objects.get(pk=int(request.data['session']))
            # print(f"hello {sess_ref.pk}")
            request.data['session'] = int(request.data['session'])

            request.data['matric'] = gen_matric()
            request.data['username'] = gen_matric()
            # request.data['session'] = "{}/{}".format(datetime.now().year, datetime.now().year + 1)
            request.data['password'] = make_password(user_data['last_name'])
            request.data['is_active'] = True

            # request.data['password'] = make_password(request.data['password'])

            serializer = UserSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                # token = Token.objects.get(id=request.user_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data['password'] = make_password(request.data['password'])
            serializer = UserSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                # token = Token.objects.get(id=request.user_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signin(request):
    data = request.data
    print(data)
    try:
        username = data['username']
        password = data['password']
        # password = make_password(data['password'])
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        user = authenticate(username=username, password=password)
        print(user)
        user_token = user.auth_token.key

    except:
        return Response(data={"status": "error", "message": "User doesn't exist"}, status=status.HTTP_401_UNAUTHORIZED)

    if user.username == "admin":
        data = {'token': user_token, 'role': user.role,
                "first_name": user.first_name, "last_name": user.last_name}
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = {'token': user_token, 'role': user.role, 'username': user.matric,
                "first_name": user.first_name, "last_name": user.last_name, "gender": user.gender,
                "other_name": user.other_name, "class": user.school_class.pk, "sesssion": user.session.pk,
                "active": user.is_active}
        return Response(data=data, status=status.HTTP_200_OK)


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class StudentList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, format=None):
        # Retrieve all students from the database
        students = User.objects.filter(role="student")

        # Serialize the student data
        serializer = UserSerializer(students, many=True)

        # Return the serialized student data as a response
        return Response(serializer.data)


class StudentDetails(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404

    def put(self, request, pk, format=None):
        # update
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response({"Message": "Student Deleted Successfully"}, status=status.HTTP_200_OK)
