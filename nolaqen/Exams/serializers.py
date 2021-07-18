from django.apps import apps
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import *

Student = apps.get_model('users', 'Student')
Courses = apps.get_model('Courses', 'Courses')
Questions = apps.get_model('Questions', 'Questions')
User = apps.get_model('users', 'User')
Groups = apps.get_model('Groups', 'Groups')


class ExamShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exams
        fields = ('name', 'id', 'end_at')


class ExamDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exams
        fields = ('description', 'start_at', 'end_at', 'name')


class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam_results
        fields = ('exam', 'student', 'results')


class CourseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['name']


class ExamDataSerializer(serializers.ModelSerializer):
    exams_courses = CourseDataSerializer()

    class Meta:
        model = Exams
        fields = ('exams_courses', 'name')
    # def to_representation(self, instance):
    #     data = super(ExamDataSerializer, self).to_representation(instance)
    #     Course = data.pop('course')
    #     for key, val in Course.items():
    #         data.update({key: val})
    #     return data


class StudentResultSerializer(serializers.ModelSerializer):
    exam = ExamDataSerializer()

    class Meta:
        model = Exam_results
        fields = ('exam', 'results')

    def to_representation(self, instance):
        data = super(StudentResultSerializer, self).to_representation(instance)
        Course = data.pop('exam')
        for key, val in Course.items():
            data.update({key: val})
        return data


# Teacher Serializer

class ExamPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam_questions
        fields = ['question']


class ExamDetailsSerializer(serializers.ModelSerializer):
    question = ExamPOSTSerializer(many=True)

    class Meta:
        model = Exams
        fields = ('name', 'course', 'start_at', 'end_at', 'Limit', 'description', 'color', 'lesson', 'question')

    def create(self, validated_data):
        question_data = validated_data.pop('question')
        exam = Exams.objects.create(**validated_data)
        for question in question_data:
            # question_obj = Questions.objects.get(pk=question)
            Exam_questions.objects.create(exam=exam, **question)
        return exam


# class ExamGroupSerializer(serializers.ModelSerializer):
#     exam = ExamPOSTSerializer()
#
#     class Meta:
#         model = Exam_groups
#         fields = ('exam' , 'group')
#

class ExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id', 'content', 'degree')


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exams
        exclude = ['id']


class UserINFOSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone')


class StudentINFOSerializer(serializers.ModelSerializer):
    user = UserINFOSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ('user', 'parent_phone')

    def to_representation(self, instance):
        data = super(StudentINFOSerializer, self).to_representation(instance)
        User = data.pop('user')
        for key, val in User.items():
            data.update({key: val})
        return data


class StudentResultSerializer(serializers.ModelSerializer):
    student = StudentINFOSerializer(read_only=True)

    class Meta:
        model = Exam_results
        fields = ('results', 'student')

    def to_representation(self, instance):
        data = super(StudentResultSerializer, self).to_representation(instance)
        Student = data.pop('student')
        for key, val in Student.items():
            data.update({key: val})
        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['id','name']


