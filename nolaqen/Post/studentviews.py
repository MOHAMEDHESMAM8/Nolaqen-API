
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .permissions import *
from .serializers import *

Student_courses = apps.get_model('Courses', 'Student_courses')
Student = apps.get_model('users', 'Student')
User = apps.get_model('users', 'User')



class Postsview(APIView):
    permission_classes = [IsStudent]
    def get(self,request,course_id):
        pass
        posts = Posts.objects.filter(course= course_id)
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
