from django.http import Http404

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import *
from .permissions import *



class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = RegisterUserSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_message, status=status.HTTP_400_BAD_REQUEST)


class AllTeachers(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeachersViewSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseNewsFeedAPIView(APIView):
    def get(self, request, course_id):
        course = Courses.objects.get(id=course_id)
        serializer = StudentCourseDataSerializer(course)
        return Response(serializer.data)


class LastPostAPIView(APIView):
    def get(self, request, course_id):
        posts = Posts.objects.filter(course=course_id).order_by('-id')[:2]
        serializer = LastPostSerializer(posts, many=True)
        return Response(serializer.data)

class LastExamAPIView(APIView):
    def get(self, request, course_id):
        exams = Exams.objects.filter(course=course_id).order_by('-id')[:2]
        serializer = LastExamSerializer(exams, many=True)
        return Response(serializer.data)

class LastLessonAPIView(APIView):
    def get(self, request, course_id):
        lesson = Lessons.objects.filter(course=course_id).order_by('-id')[:2]
        serializer = LastLessonSerializer(lesson, many=True)
        return Response(serializer.data)