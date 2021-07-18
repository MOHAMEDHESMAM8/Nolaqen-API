from django.apps import apps
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import *

Group = apps.get_model('Groups' , 'Groups')
Exams = apps.get_model('Exams', 'Exams')
Exam_questions = apps.get_model('Exams', 'Exam_questions')
Exam_groups = apps.get_model('Exams', 'Exam_groups')


class ExamQuestionsAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_answers
        fields = ('id', 'is_correct', 'answer')


class CourseQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = ('id', 'content', 'degree', 'isMultiple', 'isTrueFalse')


class WrongAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wrong_answers
        fields = ('student', 'question', 'selected_answer')


# TeacherSerializers
class QuestionAnswerPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_answers
        fields = ('is_correct', 'answer')


class ExamQuestionSerializer(serializers.ModelSerializer):
    answer = ExamQuestionsAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Questions
        fields = ('id', 'content', 'degree', 'answer')

class QuestionsPOSTSerializer(serializers.ModelSerializer):
    answer = QuestionAnswerPOSTSerializer(many=True)
 
    class Meta:
        model = Questions
        fields = ('course', 'isMultiple', 'isTrueFalse', 'content', 'degree', 'photo', 'answer')
 
    def create(self, validated_data):
        answer_data = validated_data.pop('answer')
        question = Questions.objects.create(**validated_data)
        for answer in answer_data:
            Question_answers.objects.create(question=question, **answer)
        return question
 
    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answer')
        answers = (instance.answer).all()
        answers = list(answers)
        instance.course = validated_data['course']
        instance.isMultiple = validated_data['isMultiple']
        instance.isTrueFalse = validated_data['isTrueFalse']
        instance.content = validated_data['content']
        instance.degree = validated_data['degree']
        instance.photo = validated_data['photo']
        instance.save()
 
        for answer_data in answers_data:
            x = answers.pop(0)
            x.is_correct = answer_data.get('is_correct', x.is_correct)
            x.answer = answer_data.get('answer')
            x.save()
        return instance