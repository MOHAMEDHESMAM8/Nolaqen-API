from django.apps import apps
from django.contrib.auth.models import Group
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from .models import *
from rest_framework import status
from .permissions import *

Teacher = apps.get_model('users', 'Teacher')
User = apps.get_model('users', 'User')
Student = apps.get_model('users', 'Student')


class StudentCourseLevelAPIView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        student = Student.objects.get(user=user)
        course = Courses.objects.filter(level=student.level)
        serializer = LevelCoursesSerializer(course, many=True)
        for object in serializer.data:
            course = object.get('id')
            if Student_courses.objects.filter(course=course, student=request.user.student).exists():
                object['status'] = "دخول"
                continue
            elif Requests.objects.filter(course=course, student=request.user.student).exists():
                object['status'] = "طلبك قيد المراجعة"
                continue
            else:
                object['status'] = "تسجيل"
                continue
        return Response(serializer.data, status=status.HTTP_200_OK)




class CheckCourseAPIView(APIView):
    permission_classes = [IsStudent]

    def get(self, request, course_id):
        student = Student.objects.get(user=request.user)
        student_courses = Student_courses.objects.filter(student=student, course=course_id)
        course = Courses.objects.get(id=course_id)
        teacher_phone = course.teacher.user.phone
        if student_courses.exists():
            if student_courses[0].is_active is True:
                return Response(status=status.HTTP_200_OK)
            return Response("تم تعطيل دخولك لهذا الكورس يرجى الاتصال بالرقم التالي للاستفسار {} ".format(teacher_phone),
                            status=status.HTTP_200_OK)
        else:
            if Requests.objects.filter(course=course,student=student).exists():
                return HttpResponse(
                    'تم الحجز مسبقا للاستعلام يرجي التواصل مع الأرقام التالية لتأكيد الحجز : ' + teacher_phone)
            else:
                try:
                    request = Requests(student=student, course=course)
                    request.save()
                    return HttpResponse(
                        'تم الحجز  للاستعلام يرجي التواصل مع الأرقام التالية لتأكيد الحجز : ' + teacher_phone)
                except:
                    return HttpResponse('حاول مرة أخري')


class StudentCourseAPIView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        course = Student_courses.objects.filter(student=request.user.student)
        serializer = StudentCourseSerializer(course, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CoursePointView(APIView):
    permission_classes = [IsStudent]

    def get(self, request, course):
        course_points = Student_courses.objects.get(course=course, student=request.user.student)
        serializer = CheckCourseSerializer(course_points)
        return Response(serializer.data, status=status.HTTP_200_OK)


