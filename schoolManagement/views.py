import re

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import zipfile
from django.http import HttpResponseBadRequest

from .models import SchoolSession, SchoolTerm, SchoolClass, Teacher, SchoolResult
from .serializers import SessionSerializer, TermSerializer, ClassSerializer, TeacherSerializer, ResultSerializer
from rest_framework.response import Response
from rest_framework import status

from userManagement.serializers import UserSerializer

# Create your views here.

User = get_user_model()


class Session(APIView):
    def post(self, request, format=None):
        session_data = request.data
        print(session_data)
        serializer = SessionSerializer(data=session_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        session = SchoolSession.objects.all()
        serializer = SessionSerializer(session, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SessionDetail(APIView):
    def get_object(self, pk):
        try:
            return SchoolSession.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        session = self.get_object(pk)
        serializer = SessionSerializer(session)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        # update
        sess = SchoolSession.objects.filter(status=True)
        if sess.exists():
            item = sess.first()
            item.status = False  # Update the "completed" field
            item.save()

        session = self.get_object(pk)
        serializer = SessionSerializer(session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Term(APIView):

    def post(self, request, format=None):
        term_data = request.data
        print(term_data)
        serializer = TermSerializer(data=term_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        term = SchoolTerm.objects.all()
        serializer = TermSerializer(term, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TermDetail(APIView):
    def get_object(self, pk):
        try:
            return SchoolTerm.objects.get(pk=pk)
        except:
            raise Http404

    def put(self, request, pk, format=None):
        term = SchoolTerm.objects.filter(status=True)
        if term.exists():
            item = term.first()
            item.status = False  # Update the "completed" field
            item.save()

        term = self.get_object(pk)
        serializer = TermSerializer(term, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Class(APIView):
    def post(self, request, format=None):
        class_data = request.data
        print(class_data)
        serializer = ClassSerializer(data=class_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        session = SchoolClass.objects.all()
        serializer = ClassSerializer(session, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassDetail(APIView):
    def get_object(self, pk):
        try:
            return SchoolClass.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        class_ = self.get_object(pk)
        serializer = ClassSerializer(class_)
        return Response(serializer.data)


class TeacherView(APIView):

    def post(self, request, format=None):
        teacher_data = request.data
        teacher_data['full_name'] = f"{teacher_data['title']} {teacher_data['first_name']} {teacher_data['last_name']}"
        print(teacher_data)
        class_ref = SchoolClass.objects.get(pk=teacher_data['school_class'])
        print(class_ref)
        teacher_data['school_class'] = class_ref.pk
        serializer = TeacherSerializer(data=teacher_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        teacher = Teacher.objects.all()
        serializer = TeacherSerializer(teacher, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherDetail(APIView):
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except:
            raise Http404

    def put(self, request, pk, format=None):
        # update
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def filter_student_by_class(request, pk):
    if pk:
        filtered_data = User.objects.filter(school_class=pk)
        print(filtered_data)
        serializer = UserSerializer(filtered_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        # Handle case when 'class' query parameter is not provided
        return Response(data={"error": "class id not found"}, status=status.HTTP_404_NOT_FOUND)


class Result(APIView):

    def get(self, request, format=None):
        result = SchoolResult.objects.all()
        serializer = ResultSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Get the documents from the request
        term_data = request.data['term']
        session_data = request.data['session']
        school_class_data = request.data['school_class']
        # docs = request.FILES.getlist('doc')
        zip_doc = request.FILES['doc']

        if not zipfile.is_zipfile(zip_doc):
            return HttpResponseBadRequest('Invalid ZIP file provided.')

        with zipfile.ZipFile(zip_doc, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith('/'):
                    # Skip directories
                    continue

                file_data = zip_ref.read(file_name)
                pattern = r"([A-Za-z]+)(\d+)_\d+"
                x = re.search(pattern, file_name)
                # print(x.group())

                # check if user exists with matric
                user = User.objects.get(username=x.group())
                if user is not None:
                    term = SchoolTerm.objects.get(pk=term_data)
                    print(term)
                    session = SchoolSession.objects.get(pk=session_data)
                    school_class = SchoolClass.objects.get(pk=school_class_data)
                    result = SchoolResult(session=session, matric=user.matric, term_name=term.term_name,
                                          session_name=session.session_name, class_name=school_class.name, term=term,
                                          school_class=school_class, user=user,
                                          doc=file_name, )
                    result.save()
                else:
                    return HttpResponseBadRequest(f'{x.group()} doesnt exists')

        return Response(data={"message": "Documents uploaded successfully."}, status=status.HTTP_200_OK)


@api_view(['GET'])
def filter_result_by_class(request, pk):
    # something
    if pk:
        filtered_data = SchoolResult.objects.filter(school_class=pk)
        print(filtered_data)
        serializer = ResultSerializer(filtered_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        # Handle case when 'class' query parameter is not provided
        return Response(data={"error": "class id not found"}, status=status.HTTP_404_NOT_FOUND)
