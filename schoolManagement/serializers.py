from rest_framework import serializers
from .models import SchoolTerm, SchoolSession


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolTerm
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSession
        fields = "__all__"
