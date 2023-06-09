from rest_framework import serializers
from .models import SchoolTerm, SchoolSession, SchoolClass, Teacher, Result


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolTerm
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSession
        fields = "__all__"


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
