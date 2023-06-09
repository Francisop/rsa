from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models import Q

from .models import SchoolSession, SchoolTerm, SchoolClass, Teacher, SchoolResult
from .serializers import SessionSerializer, TermSerializer, ClassSerializer, TeacherSerializer, ResultSerializer
from rest_framework.response import Response
from rest_framework import status

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
def filter_student_by_class(request):
    # term = request.query_params.get('term')
    # session = request.query_params.get('session')
    class_id = request.query_params.get('class')
    # Use the value of the 'class' query parameter as needed
    if class_id:
        filtered_data = User.objects.filter(school_class=class_id)
        print(filtered_data)
        # Perform actions based on the value
        # ...
        return Response(data={"data": filtered_data}, status=status.HTTP_200_OK)
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
        term = request.data['term']
        session = request.data['session']
        school_class = request.data['school_class']
        docs = request.FILES.getlist('doc')

        # user = User.objects.get(name=user_name)  # Assuming there's a single user with the given name

        for document in docs:
            user = User.objects.filter(username=document.name)
            if user is not None:
                if user:
                    result = SchoolResult(user=user, document=document, session=session, school_class=school_class,
                                          term=term)
                    print(result)
                    serializer = ResultSerializer(data=result)
                    serializer.is_valid(raise_exception=True)
                    print(serializer)
                    serializer.save()

            # Create a new document record

            # Save the document record

        return Response(data={"message": "Documents uploaded successfully."}, status=status.HTTP_200_OK)
