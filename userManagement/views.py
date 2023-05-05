from django.shortcuts import render
from django.contrib.auth import get_user_model
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
        # request.data._mutable = True
        user_data = request.data
        print(gen_matric())
        # print(request.data)
        if user_data['role'] == 'student':
            student_pass = user_data['full_name'].split()
            print(student_pass[1])
            request.data['matric'] = gen_matric()
            request.data['username'] = gen_matric()
            request.data['session'] = "{}/{}".format(datetime.now().year,datetime.now().year+1)
            request.data['password'] = make_password(student_pass[1])
            # request.data['password'] = make_password(request.data['password'])
            # request.data._mutable = False
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
            # request.data._mutable = False
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
    try:
        username = data['username']
        password = data['password']
        # password = make_password(data['password'])
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        user = authenticate(username=username, password=password)
        print(user.role)
        # user = User.objects.get(Q(email=email) & Q(password=password))
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        if user is not None:
            user_token = user.auth_token.key
        else:
            return Response({"message": "User doesn't exist"})
    except:
        return Response({"message": "unknown error"})

    data = {'token': user_token, 'role': user.role, 'username': user.matric,
            "full_name": user.full_name, "sesssion":user.session}
    return Response(data=data, status=status.HTTP_200_OK)




