from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from .models import *
from rest_framework import status
from .permissions import *


Student_courses = apps.get_model('Courses', 'Student_courses')
User = apps.get_model('users', 'User')
Student = apps.get_model('users', 'Student')
