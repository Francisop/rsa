from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView

from .models import SchoolSession, SchoolTerm
from .serializers import SessionSerializer, TermSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

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

    def put(self, request, pk, format=None):
        session = self.get_object(pk)
        serializer = SessionSerializer(session, data=request.data)
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
        term = self.get_object(pk)
        serializer = TermSerializer(term, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
