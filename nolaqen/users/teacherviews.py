from django.db.models import Exists, OuterRef
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404

from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
from .models import *
from .permissions import *


class ALlStudentCourseView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def get(self, request, course):
        self.check_owner(request=request, obj=course, model=Courses)
        students = Student_courses.objects.filter(course=course)
        serializer = ALlStudentCourseSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentInfoView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def get(self, request, course, student):
        self.check_owner(request=request, obj=course, model=Courses)
        student_obj = Student_courses.objects.get(course=course,student=student)
        serializer = ALlStudentCourseSerializer(student_obj)
        return Response(serializer.data,status=status.HTTP_200_OK)


class ActivateStudentsView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def post(self, request, course):
        self.check_owner(request=request, obj=course, model=Courses)
        course_obj = Courses.objects.get(id=course)
        if all(isinstance(x, int) for x in request.data):
            for id in request.data:
                object = Student.objects.get(id=id)
                student = Student_courses.objects.get(student=object, course=course_obj)
                student.is_active = True
                student.save()
            return HttpResponse("تم تفعيل الطلاب بنجاح", status=status.HTTP_200_OK)
        return HttpResponse('لم يتم اضافة الطلاب الرجاء التاكد من البيانات المدخلة', status=status.HTTP_400_BAD_REQUEST)


class DeactivateStudentsView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def post(self, request, course):
        self.check_owner(request=request, obj=course, model=Courses)
        course_obj = Courses.objects.get(id=course)
        if all(isinstance(x, int) for x in request.data):
            for id in request.data:
                object = Student.objects.get(id=id)
                student = Student_courses.objects.get(student=object, course=course_obj)
                student.is_active = False
                student.save()
            return HttpResponse("تم تعطيل الطلاب بنجاح", status=status.HTTP_200_OK)
        return HttpResponse('لم يتم اضافة الطلاب الرجاء التاكد من البيانات المدخلة', status=status.HTTP_400_BAD_REQUEST)


class ChangeGroupView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def post(self, request, group):
        self.check_owner(request=request, obj=group, model=Groups)
        course = Groups.objects.get(id=group).course
        group_obj = Groups.objects.get(id=group)
        if all(isinstance(x, int) for x in request.data):
            for id in request.data:
                object = Student.objects.get(id=id)
                student = Student_courses.objects.get(course=course, student=object)
                student.group = group_obj
                student.save()
            return HttpResponse("تم تغير مجموعة الطلاب المختارة الى {}".format(group_obj.name),
                                status=status.HTTP_200_OK)
        return HttpResponse('لم يتم اضافة الطلاب الرجاء التاكد من البيانات المدخلة', status=status.HTTP_400_BAD_REQUEST)


class StudentAllLessonsView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def get(self, request, course, student):
        self.check_owner(request=request, obj=course, model=Courses)
        lessons = Lessons.objects.filter(course=course).values_list('id', flat=True)
        student = Lesson_views.objects.filter(lesson__in=lessons, student=student)
        serializer = ALlLessonsSerializer(student, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentAllResultsView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def get(self, request, course, student):
        self.check_owner(request=request, obj=course, model=Courses)
        exams = Exams.objects.filter(course=course).values_list('id', flat=True)
        student = Exam_results.objects.filter(exam__in=exams, student=student)
        serializer = AllStudentResults(student, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonsBeforeStudentView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def get(self, request, course, student):
        self.check_owner(request=request, obj=course, model=Courses)
        student_time = Student_courses.objects.get(course=course, student=student).created_at
        lessons = Lessons.objects.filter(
            ~Exists(Student_lessons.objects.filter(lesson=OuterRef('pk'), student=student)),
            course=course, created_at__lt=student_time
        )
        serializer = LessonsBeforeStudentSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonsAddedBeforeView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def get(self, request, course, student):
        self.check_owner(request=request, obj=course, model=Courses)
        lessons = Lessons.objects.filter(course=course)
        student_lessons = Student_lessons.objects.filter(lesson__in=lessons, student=student)
        serializer = AddedLessonsSerializer(student_lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddLessonsView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def post(self, request, course, student):
        self.check_owner(request=request, obj=course, model=Courses)
        student = Student.objects.get(id=student)

        check_arr = request.data.pop('check')
        if all(isinstance(x, int) for x in check_arr):
            for id in check_arr:
                lesson = Lessons.objects.get(id=id)
                Student_lessons.objects.create(student=student, lesson=lesson)
        else:
            return HttpResponse('لم يتم اضافة الحصص الرجاء التاكد من البيانات المدخلة',
                                status=status.HTTP_400_BAD_REQUEST)
        uncheck_arr = request.data.pop('uncheck')
        if all(isinstance(x, int) for x in uncheck_arr):
            for id in uncheck_arr:
                object = Student_lessons.objects.filter(student=student, lesson=id)
                object.delete()
        else:
            return HttpResponse('لم يتم اضافة الحصص الرجاء التاكد من البيانات المدخلة',
                                status=status.HTTP_400_BAD_REQUEST)
        return Response("تم اضافة الحصص  بنجاح", status=status.HTTP_200_OK)

class NotificationAPIView(APIView):
    def get(self, request):
        student = Student.objects.get(user=request.user)
        student_course = Student_courses.objects.filter(student=student)
        notification_list = []
        notify = Notification.objects.filter(course__in=student_course.values_list('course'), type=3)
        notify2 = Notification.objects.filter(course__in=student_course.values_list('course'), student=student)
        notify3 = Notification.objects.filter(course__in=student_course.values_list('course'), type=4,
                                              group__in=student_course.values_list('group', flat=True))
        if len(notify) != 0:
            notification_list.append(notify.values_list('message', 'created_at', 'viewed'))
            notification_list.append(notify2.values_list('message', 'created_at', 'viewed'))
            notification_list.append(notify3.values_list('message', 'created_at', 'viewed'))
        else:
            pass
        new_list = list(itertools.chain(*notification_list))
        keys = ['message', 'created_at', 'viewed']
        out = [dict(zip(keys, sublst)) for sublst in new_list]
        return Response(out)


class MonthCountAPIView(APIView):
    permission_classes = [IsTeacher]


    def get(self, request, month):
        teacher = Teacher.objects.get(id=request.user.id)
        allCourses = Courses.objects.filter(teacher=teacher)
        list_json = []

        for course in allCourses:
            course_log = Logs.objects.filter(course=course, created_at__month=month)
            students = course_log.count()
            months = list(course_log.values_list('month_number', flat=True))
            total = 0
            for num in months:
                total += num
            data = {'course_name': course.name, "total": total, "students": students}
            list_json.append(data)
        return JsonResponse(list_json, content_type ="application/json" , safe=False)


class LogStudentAPIView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request, month):
        teacher = Teacher.objects.get(id=request.user.id)
        allCourses = Courses.objects.filter(teacher=teacher)
        logs = Logs.objects.filter(course_in=  allCourses, created_at_month=month)
        serializer = LogsStudentSerializer(logs, many=True)
        return Response(serializer.data)


class StudentPointsAPIView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def post(self, request, course):
        self.check_owner(request=request, obj=course, model=Courses)
        course_obj = Courses.objects.get(id=course)

        student = Student.objects.get(id=request.data.pop('student'))
        month = request.data.get('month_number')
        Logs.objects.create(student=student, course=course_obj, month_number=month)
        lesson_num = course_obj.lesson_num
        points = lesson_num * month
        student_point = Student_courses.objects.get(student=student, course=course_obj)
        student_point.point += points
        student_point.save()
        return Response(" تم اضـافة النقـاط ", status=status.HTTP_200_OK)


#logs for student profile
class StudentLogsView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def get(self, request, course,student):
        self.check_owner(request=request, obj=course, model=Courses)
        logs = Logs.objects.filter(course=course, student=student)
        serializer = StudentLogsProfile(logs, many=True)
        return Response(serializer.data)