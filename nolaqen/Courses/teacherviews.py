from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
from .permissions import *
from django.apps import apps
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import json
from django.shortcuts import HttpResponse, get_object_or_404

Teacher = apps.get_model('users', 'Teacher')
Groups = apps.get_model('Groups', 'Groups')


@api_view(['GET'])
@permission_classes((IsTeacher))
def StudentCourseNumber(request):
    teacher = Teacher.objects.get(user=request.user)
    courses = Courses.objects.filter(teacher=teacher)
    list = {}
    i = 0
    while i <= courses.count() - 1:
        for n in courses.values_list('id', flat=True):
            student_number = Student_courses.objects.filter(course=n).count()
            list[courses[i].name] = student_number
            i += 1
    json_format = json.dumps(list)
    return HttpResponse(json_format, content_type='application/json; charset=utf-8')


class AllCourses(APIView):
    permission_classes = [IsTeacher]

    def get(self, request):
        courses = Courses.objects.filter(teacher=request.user.teacher.id)
        serializer = TeacherCoursesSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentCourseNumberAPIView(APIView):
    def get(self, request, course):
        course = Courses.objects.filter(id=course)
        students = Student_courses.objects.filter(course__in=course)
        serializer = StudentCourseNumberSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestsView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, course):
        self.check_owner(request=request, obj=course, model=Courses)
        requests = Requests.objects.filter(course=course)
        serializer = AllRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AcceptRequest(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def post(self, request, course):
        self.check_owner(request=request, obj=course, model=Courses)
        course = Courses.objects.get(id=course)
        for id in request.data:
            student_request = Requests.objects.get(id=id)
            Student_courses.objects.create(course=course, student=student_request.student,
                                           point=request.user.teacher.lesson_num)
            student_request.delete()
        return HttpResponse('تم قبول الطلاب بنجاح', status=status.HTTP_200_OK)


class RejectRequest(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def post(self, request, course):
        self.check_owner(request=request, obj=course, model=Courses)
        course = Courses.objects.get(id=course)
        for id in request.data:
            student_request = Requests.objects.get(id=id)
            student_request.delete()
        return HttpResponse('تم رفض الطلاب بنجاح', status=status.HTTP_200_OK)
