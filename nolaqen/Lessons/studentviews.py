from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db.models import Q
from .permissions import *

Student_courses = apps.get_model('Courses', 'Student_courses')
Student = apps.get_model('users', 'Student')
User = apps.get_model('users', 'User')

class StudentLessonAPIView(APIView):
    permission_classes = [IsStudent]
    def get(self, request, course_id):
        user = Student.objects.get(user=request.user)
        student = Student_courses.objects.get(course=course_id, student=user.id)
        lessonGroups_obj = Lesson_groups.objects.filter(group=student.group, ).values_list('lesson', flat=True)
        lesson_obj = Lessons.objects.filter(id__in=lessonGroups_obj, created_at__gt=student.created_at,
                                            course=course_id)
        custom_Lessons = Student_lessons.objects.filter(student=user.id).values_list('lesson', flat=True)
        lesson_obj2 = Lessons.objects.filter(id__in=custom_Lessons, course=course_id)
        all_lessons = lesson_obj.union(lesson_obj2).order_by('created_at')
        serializer = LessonSerializer(all_lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class StudentLessonViewCheck(APIView):
    permission_classes = [IsStudent]
    def get(self, request,lesson):
        user = Student.objects.get(user=request.user)
        check = Lesson_views.objects.filter(student=user, lesson=lesson)
        course = Lessons.objects.get(pk=lesson).course
        lesson_obj = Lessons.objects.get(pk=lesson)
        student_course = Student_courses.objects.get(student=user, course=course)
        default = views.objects.all().first()
        if default.views == True:
            if not check.exists():
                if student_course.point == 0:
                    return HttpResponse("لا تمتلك نقاط كافية")
                else:
                    view = Lesson_views(student=user, lesson=lesson_obj,views=(default.single_view-1))
                    view.save()
                    student_course.point = student_course.point - 1
                    student_course.save()
                    return HttpResponse("تم خصم نقطة متبقى لديك {}".format(student_course.point))
            else:
                student_views = Lesson_views.objects.get(student=user, lesson=lesson)
                if student_views.views == 0:
                    if student_course.point == 0:
                        return HttpResponse("لا تمتلك نقاط كافية")
                    else:
                        student_course.point = student_course.point - 1
                        student_views.views = student_views.views + (default.single_view - 1)
                        student_course.save()
                        student_views.save()
                        return HttpResponse("تم خصم نقطة لديك {} مشاهدات لهذا الفيديو".format(student_views.views))
                else:
                    student_views.views = student_views.views - 1
                    student_views.save()
                    return HttpResponse("تم خصم مشاهدة لديك {} مشاهدات لهذا الفيديو".format(student_views.views))
        else:
            if not check.exists():
                if student_course.point == 0:
                    return HttpResponse("لا تمتلك نقاط كافية")
                else:
                    view = Lesson_views(student=user, lesson=lesson_obj,views=0)
                    view.save()
                    student_course.point = student_course.point - 1
                    student_course.save()
                    return HttpResponse("تم خصم نقطة متبقى لديك {}".format(student_course.point))
            else:
               return HttpResponse(status=status.HTTP_200_OK)



