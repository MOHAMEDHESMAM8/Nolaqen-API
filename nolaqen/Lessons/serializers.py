from django.apps import apps
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import *

Student_courses = apps.get_model('Courses', 'Student_courses')
Student = apps.get_model('users', 'Student')
User = apps.get_model('users', 'User')
Groups = apps.get_model('Groups', 'Groups')



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ('id', 'name', 'description', 'created_at')


class StudentPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_courses
        fields = ['point']


class TeacherLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ('id', 'name', 'created_at', 'description')


class UpdateLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['name', 'description']
        read_only_fields = ['created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = ['id','user']

    def to_representation(self, instance):
        data = super(StudentSerializer, self).to_representation(instance)
        User = data.pop('user')
        for key, val in User.items():
            data.update({key: val})
        return data


class LessonViewsSerialier(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = Lesson_views
        fields = ['created_at','student']
    def to_representation(self, instance):
        data = super(LessonViewsSerialier, self).to_representation(instance)
        student = data.pop('student')
        for key, val in student.items():
            data.update({key: val})
        return data



class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['id', 'name']