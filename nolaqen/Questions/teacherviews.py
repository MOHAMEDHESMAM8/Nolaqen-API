from django.http import HttpResponse
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .permissions import *
from rest_framework import status
from django.db.models import Count, Case, When
from django.shortcuts import get_object_or_404

Exams = apps.get_model('Exams', 'Exams')
Exam_questions = apps.get_model('Exams', 'Exam_questions')
Group = apps.get_model('Groups' , 'Groups')
Exam_groups = apps.get_model('Exams', 'Exam_groups')



class QuestionTeacherPostAPIView(APIView):
    permission_classes = [CourseOwner]
    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)
    def get(self, request, course_id):
        self.check_owner(request=request, obj=course_id, model=Courses)
        questions = Questions.objects.filter(course=course_id)
        serializer = CourseQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, course_id):
        self.check_owner(request=request, obj=course_id, model=Courses)
        serializer = QuestionsPOSTSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionsUpdateAPIView(APIView):
    permission_classes = [Owner]
    
    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get_object(self,request, id):
        try:
            self.check_owner(request=request, obj=id, model=Questions)
            return Questions.objects.get(id=id)
        except Questions.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        question = self.get_object(request = request,id=id)
        serializer = QuestionsPOSTSerializer(question)
        return Response(serializer.data)

    def put(self, request, id):
        question = self.get_object(request = request,id=id)
        serializer = QuestionsPOSTSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        question = self.get_object(request = request,id=id)
        question.delete()
        return Response("تم مسح السؤال بنجاح", status=status.HTTP_200_OK)


# this is not correct call me
# class StudentWrongAnswersAPIView(APIView):
#     def get(self, request, exam):
#         exam = Exams.objects.filter(id=exam)
#         exam_question = Exam_questions.objects.filter(exam__in=exam)
#         questions = Questions.objects.filter(id__in=exam_question)
#         wrong_answer = Wrong_answers.objects.filter(question__in=questions.values_list('id', flat=True))
#         answer = Question_answers.objects.filter(question__in=questions , is_correct=False)
#         for i in range(len(wrong_answer)):
#             if answer == wrong_answer:
#
#         return HttpResponse(answer)





