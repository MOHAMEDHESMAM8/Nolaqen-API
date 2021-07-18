from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from .models import *
from rest_framework import status
from .permissions import *


Student_courses = apps.get_model('Courses', 'Student_courses')
User = apps.get_model('users', 'User')
Student = apps.get_model('users', 'Student')



class StudentExamAPIView(APIView):
    permission_classes=[IsStudent]
    def get(self, request,course_id):
        student = Student_courses.objects.get(course = course_id , student=request.user.id)
        examGroups_obj = Exam_groups.objects.filter(group = student.group)
        exam_obj = Exams.objects.filter(pk__in=examGroups_obj.values_list('exam', flat=True))
        serializer = ExamSerializer(exam_obj, many=True)
        return Response(serializer.data)


class ExamDetailsAPIView(APIView):
    permission_classes=[IsStudent]
    def get(self, request, exam_id):
        exam_obj = Exams.objects.filter(id=exam_id)
        serializer = ExamDetailsSerializer(exam_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExamResultAPIView(APIView):
    permission_classes=[StudentPost]
    def post(self,request):
        serializer = ExamResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentResultAPIiew(APIView):
    permission_classes=[IsStudent]

    def get(self, request):
        student = Student.objects.get(user=request.user)
        student_result = Exam_results.objects.filter(student=student)
        serializer = StudentResultSerializer(student_result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


