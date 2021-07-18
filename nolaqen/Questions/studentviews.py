from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from rest_framework import status
from .permissions import *

Exam_questions = apps.get_model('Exams', 'Exam_questions')


class ExamQuestionsAPIView(APIView):
    permission_classes = [IsStudent]

    def get(self, request, exam_id):
        exam = Exam_questions.objects.filter(exam=exam_id)
        examquestions_obj = Questions.objects.filter(id__in=exam.values_list('question', flat=True))
        serializer = ExamQuestionSerializer(examquestions_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WrongAnswerAPIView(APIView):
    permission_classes = [StudentPost]

    def post(self, request):
        serializer = WrongAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
