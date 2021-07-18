from django.apps import apps
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import *

Student = apps.get_model('users', 'Student')
Student_courses = apps.get_model('Courses', 'Student_courses')
Courses = apps.get_model('Courses', 'Courses')
Questions = apps.get_model('Questions', 'Questions')
User = apps.get_model('users', 'User')


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = ['id', 'user']

    def to_representation(self, instance):
        data = super(StudentSerializer, self).to_representation(instance)
        User = data.pop('user')
        for key, val in User.items():
            data.update({key: val})
        return data

