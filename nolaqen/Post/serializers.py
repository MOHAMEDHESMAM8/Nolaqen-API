from django.apps import apps
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import *

Courses = apps.get_model('Courses', 'Courses')
Teacher= apps.get_model('users', 'Teacher')
User = apps.get_model('users' ,'User')


class UserTeacherViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class TeachersSerializer(serializers.ModelSerializer):
    user = UserTeacherViewSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'photo']

    def to_representation(self, instance):
        data = super(TeachersSerializer, self).to_representation(instance)
        user = data.pop('user')
        for key, val in user.items():
            data.update({key: val})
        return data

class CourseSerializer(serializers.ModelSerializer):
    teacher = TeachersSerializer()

    class Meta:
        model = Courses
        fields = ['teacher']

    def to_representation(self, instance):
        data = super(CourseSerializer, self).to_representation(instance)
        teacher = data.pop('teacher')
        for key, val in teacher.items():
            data.update({key: val})
        return data
class  PostSerializer(serializers.ModelSerializer):
    course=CourseSerializer()
    class Meta:
        model = Posts
        fields = ['course','content','created_at']
    def to_representation(self, instance):
        data = super(PostSerializer, self).to_representation(instance)
        course = data.pop('course')
        for key, val in course.items():
            data.update({key: val})
        return data


class PostPost(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = "__all__"
