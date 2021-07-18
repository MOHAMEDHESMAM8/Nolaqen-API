from django.db.models import Exists, OuterRef
from django.http import HttpResponse, Http404
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
Group = apps.get_model('Groups', 'Groups')


class ExamPOSTAPIView(APIView):
    permission_classes = [IsTeacher]

    def post(self, request):
        serializer = ExamDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Exam Question for specific Course
class ExamQuestionAPIView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, course_id):
        self.check_owner(request=request, obj=course_id, model=Courses)
        question = Questions.objects.filter(course=course_id)
        serializer = ExamQuestionSerializer(question, many=True)
        return Response(serializer.data)


class AllExamsAPIView(APIView):
    permission_classes = [CourseOwner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, course_id):
        self.check_owner(request=request, obj=course_id, model=Courses)
        exam = Exams.objects.filter(course=course_id)
        serializer = ExamShowSerializer(exam, many=True)
        return Response(serializer.data)


class ExamsUpdateAPIView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get_object(self, request, id):
        try:
            self.check_owner(request=request, obj=id, model=Exams)
            return Exams.objects.get(id=id)
        except Exams.DoesNotExist:
            raise Http404

    def get(self, request, id):
        exam = self.get_object(request=request, id=id)
        serializer = ExamSerializer(exam)
        return Response(serializer.data)

    def put(self, request, id):
        exam = self.get_object(request=request ,id=id)
        serializer = ExamSerializer(exam, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        exam = self.get_object(request=request, id=id)
        exam.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllStudentResultAPIView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, exam_id):
        self.check_owner(request=request, obj=exam_id, model=Exams)
        results = Exam_results.objects.filter(exam=exam_id)
        serializer = StudentResultSerializer(results, many=True)
        return Response(serializer.data)


class ExamUncheckedGroupsView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, exam):
        self.check_owner(request=request, obj=exam, model=Exams)
        exam_obj = Exams.objects.get(id=exam)
        course = exam_obj.course
        group = Group.objects.filter(
            ~Exists(Exam_groups.objects.filter(group=OuterRef('pk'), exam=exam_obj)),
            course=course,
        )
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonCheckedGroupsView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, exam):
        self.check_owner(request=request, obj=exam, model=Exams)
        groups = Exam_groups.objects.filter(exam=exam).values_list('group', flat=True)
        group = Group.objects.filter(id__in=groups)
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddLessonGroupsView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def post(self, request, exam):
        self.check_owner(request=request, obj=exam, model=Exams)
        exam_obj = Exams.objects.get(id=exam)
        check_arr = request.data.pop('check')
        if all(isinstance(x, int) for x in check_arr):
            for id in check_arr:
                group = Group.objects.get(id=id)
                Exam_groups.objects.create(exam=exam_obj, group=group)
        else:
            return HttpResponse('لم يتم اضافة الامتحان الرجاء التاكد من البيانات المدخلة',
                                status=status.HTTP_400_BAD_REQUEST)
        uncheck_arr = request.data.pop('uncheck')
        if all(isinstance(x, int) for x in uncheck_arr):
            for id in uncheck_arr:
                object = Exam_groups.objects.get(exam=exam_obj, group=id)
                object.delete()
        else:
            return HttpResponse('لم يتم اضافة الامتحان الرجاء التاكد من البيانات المدخلة',
                                status=status.HTTP_400_BAD_REQUEST)
        return Response("تم اضافة الامتحانات بنجاح للمجموعات المحددة", status=status.HTTP_200_OK)

class CheckedQuestionsForUpdateView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def get(self, request, exam):
        self.check_owner(request=request, obj=exam, model=Exams)
        questions_id =  Exam_questions.objects.filter(exam= exam).values_list('question',flat=True)
        questions = Questions.objects.filter(id__in = questions_id)
        serializer = ExamQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UncheckedQuestionsForUpdateView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(self.request, message)

    def get(self, request, exam):
        self.check_owner(request=request, obj=exam, model=Exams)
        exam_obj = Exams.objects.get(id=exam)
        course = exam_obj.course
        questions = Questions.objects.filter(
            ~Exists(Exam_questions.objects.filter(question=OuterRef('pk'), exam=exam_obj)),
            course=course,
        )
        serializer = ExamQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddQuestionsForExamView(APIView):
    permission_classes = [Owner]

    def check_owner(self, request, obj, model):
        message = get_object_or_404(model, id=obj)
        self.check_object_permissions(request, message)

    def post(self, request, exam):
        self.check_owner(request=request, obj=exam, model=Exams)
        exam_obj = Exams.objects.get(id=exam)
        check_arr = request.data.pop('check')
        if all(isinstance(x, int) for x in check_arr):
            for id in check_arr:
                question = Questions.objects.get(id=id)
                Exam_questions.objects.create(exam=exam_obj, question=question)
        else:
            return HttpResponse('لم يتم اضافة الاسئلة الرجاء التاكد من البيانات المدخلة',
                                status=status.HTTP_400_BAD_REQUEST)
        uncheck_arr = request.data.pop('uncheck')
        if all(isinstance(x, int) for x in uncheck_arr):
            for id in uncheck_arr:
                object = Exam_questions.objects.get(exam=exam_obj, question=id)
                object.delete()
        else:
            return HttpResponse('لم يتم اضافة الامتحان الرجاء التاكد من البيانات المدخلة',
                                status=status.HTTP_400_BAD_REQUEST)
        return Response("تم اضافة الامتحانات بنجاح للمجموعات المحددة", status=status.HTTP_200_OK)