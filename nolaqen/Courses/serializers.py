from django.apps import apps
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import *

User = apps.get_model('users', 'User')
Teacher = apps.get_model('users', 'Teacher')
Student = apps.get_model('users', 'Student')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user']

    def to_representation(self, instance):
        data = super(TeacherSerializer, self).to_representation(instance)
        User = data.pop('user')
        for key, val in User.items():
            data.update({key: val})
        return data


class LevelCoursesSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Courses
        fields = ['id' , 'level' , 'teacher' , 'photo']

    def to_representation(self, instance):
        data = super(LevelCoursesSerializer, self).to_representation(instance)
        teacher = data.pop('teacher')
        for key, val in teacher.items():
            data.update({key: val})
        return data


class CheckCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_courses
        fields = ['point']


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = ['student', 'course', 'created_at']


class CourseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['id', 'name', 'photo']


class StudentCourseSerializer(serializers.ModelSerializer):
    course = CourseDetailsSerializer()

    class Meta:
        model = Student_courses
        fields = ['course']

    def to_representation(self, instance):
        data = super(StudentCourseSerializer, self).to_representation(instance)
        Course = data.pop('course')
        for key, val in Course.items():
            data.update({key: val})
        return data


class TeacherCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['id', 'name']


class RequestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','phone']


class StudentSerializer(serializers.ModelSerializer):
    user = RequestUserSerializer()
    class Meta:
        model = Student
        fields = ['user','parent_phone']

    def to_representation(self, instance):
        data = super(StudentSerializer, self).to_representation(instance)
        User = data.pop('user')
        for key, val in User.items():
            data.update({key: val})
        return data


class AllRequestSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = Requests
        fields = ['id','student', 'created_at']

    def to_representation(self, instance):
        data = super(AllRequestSerializer, self).to_representation(instance)
        student = data.pop('student')
        for key, val in student.items():
            data.update({key: val})
        return data
