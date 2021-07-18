from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse, get_object_or_404
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db.models import Q, Exists, OuterRef
from .permissions import *

Courses = apps.get_model('Courses', 'Courses')
Student = apps.get_model('users', 'Student')
User = apps.get_model('users', 'User')


class AllTeacherLessons(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, course):
        self.check_owner(request=request, obj=course, model=Courses)
        courses = Lessons.objects.filter(course=course)
        serializer = TeacherLessonsSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateDeleteLesson(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, lesson):
        self.check_owner(request=request, obj=lesson, model=Lessons)
        lesson = Lessons.objects.get(id=lesson)
        serializer = UpdateLessonSerializer(lesson)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, lesson):
        self.check_owner(request=request, obj=lesson, model=Lessons)
        lesson = Lessons.objects.get(id=lesson)
        serializer = UpdateLessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, lesson):
        lesson = Lessons.objects.get(id=lesson)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonViews(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, lesson):
        self.check_owner(request=request, obj=lesson, model=Lessons)
        lesson_views = Lesson_views.objects.filter(lesson=lesson)
        serializer = LessonViewsSerialier(lesson_views, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonUncheckedGroupsView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, lesson):
        self.check_owner(request=request, obj=lesson, model=Lessons)
        lesson_obj = Lessons.objects.get(id=lesson)
        course = lesson_obj.course
        group = Groups.objects.filter(
            ~Exists(Lesson_groups.objects.filter(group=OuterRef('pk'), lesson=lesson_obj)),
            course=course,
        )
        serializer = GroupsSerializer(group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonCheckedGroupsView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, lesson):
        self.check_owner(request=request, obj=lesson, model=Lessons)
        groups = Lesson_groups.objects.filter(lesson=lesson).values_list('group', flat=True)
        group = Groups.objects.filter(id__in=groups)
        serializer = GroupsSerializer(group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddLessonGroupsView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def post(self, request, lesson):
        self.check_owner(request=request, obj=lesson, model=Lessons)
        lesson_obj = Lessons.objects.get(id=lesson)

        check_arr = request.data.pop('check')
        if all(isinstance(x, int) for x in check_arr):
            for id in check_arr:
                group = Groups.objects.get(id=id)
                Lesson_groups.objects.create(lesson=lesson_obj, group=group)
        else:
            return HttpResponse('لم يتم اضافة الحصة الرجاء التاكد من البيانات المدخلة',
                                status=status.HTTP_400_BAD_REQUEST)
        uncheck_arr = request.data.pop('uncheck')
        if all(isinstance(x, int) for x in uncheck_arr):
            for id in uncheck_arr:
                object = Lesson_groups.objects.get(lesson=lesson_obj, group=id)
                object.delete()
        else:
            return HttpResponse('لم يتم اضافة الحصة الرجاء التاكد من البيانات المدخلة',
                                status=status.HTTP_400_BAD_REQUEST)
        return Response("تم اضافة الحصة بنجاح للمجموعات المحددة", status=status.HTTP_200_OK)