from django.http import HttpResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from rest_framework import status
from .permissions import *
from django.apps import apps

Questions = apps.get_model('Questions', 'Questions')
Teacher = apps.get_model('users', 'Teacher')
Courses = apps.get_model('Courses', 'Courses')
Student_courses = apps.get_model('Courses', 'Student_courses')


class CourseGroupsView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, course):
        self.check_owner(request=request, obj=course, model=Courses)
        groups = Groups.objects.filter(course=course)
        serializer = GroupsSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetStudentCourses(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, course):
        self.check_owner(request=request, obj=course, model=Courses)
        students = Student_courses.objects.filter(course=course, group__isnull=True).values_list('student', flat=True)
        students_obj = Student.objects.filter(id__in=students)
        serializer = StudentSerializer(students_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewGroupView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def post(self, request, course):
        self.check_owner(request=request, obj=course, model=Courses)
        name = request.data.pop('name')
        course_obj = Courses.objects.get(id=course)
        new_group = Groups.objects.create(name=name, course=course_obj)
        data = request.data.pop('students')
        if all(isinstance(x, int) for x in data ):
            for id in data:
                student = Student.objects.get(id=id)
                object = Student_courses.objects.get(course=course, student=student)
                object.group = new_group
                object.save()
            return HttpResponse('تم اضافة الطلاب بنجاح', status=status.HTTP_200_OK)
        return HttpResponse('لم يتم اضافة الطلاب الرجاء التاكد من البيانات المدخلة', status=status.HTTP_400_BAD_REQUEST)

class GetGroupStudentView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, group):
        self.check_owner(request=request, obj=group, model=Groups)
        students = Student_courses.objects.filter(group=group).values_list('student', flat=True)
        students_obj = Student.objects.filter(id__in=students)
        serializer = StudentSerializer(students_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateDeleteGroupView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, group):
        self.check_owner(request=request, obj=group, model=Groups)
        group = Groups.objects.get(id=group)
        serializer = GroupsSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, group):
        self.check_owner(request=request, obj=group, model=Groups)
        group = Groups.objects.get(id=group)
        serializer = GroupsSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("تم تغير اسم المجموعة بنجاح", status=status.HTTP_200_OK)
        return Response("لم تغير اسم المجموعة بنجاح", status=status.HTTP_200_OK)

    def delete(self, request, group):
        self.check_owner(request=request, obj=group, model=Groups)
        group_obj = Groups.objects.filter(id=group)
        if group_obj[0].student_courses_groups.exists():
            return Response("لا يمكن حذف المجموعة وبها طلاب يرجى تغير مجموعة الطلاب اولا ثم اعادة المحاولة",
                            status=status.HTTP_200_OK)
        group_obj.delete()
        return Response("تم حذف المجموعة بنجاح",
                        status=status.HTTP_204_NO_CONTENT)