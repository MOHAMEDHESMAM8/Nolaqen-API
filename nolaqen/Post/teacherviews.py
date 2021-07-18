from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse, get_object_or_404
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db.models import Q
from .permissions import*

from .serializers import*

Courses = apps.get_model('Courses', 'Courses')
Student = apps.get_model('users', 'Student')
User = apps.get_model('users', 'User')



class AddPostView(APIView):
    permission_classes = [IsTeacher]
    def post(self,request):
        serializer = PostPost(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)




