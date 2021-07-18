from os import name
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .studentviews import *
from .teacherviews import *


urlpatterns = [
    path('courses' , StudentCourseLevelAPIView.as_view() , name='courses'),
    path('check/<int:course_id>', CheckCourseAPIView.as_view() , name='check'),
    path('student_course', StudentCourseAPIView.as_view() , name='student_course'),

    #teacher urls
    path('student_number', csrf_exempt(StudentCourseNumber) , name='student_number'),# student number
    path('teacher-courses', AllCourses.as_view() , name='Teacher Courses'),# show id and name for teacher courses
    path('requests/<int:course>', RequestsView.as_view(), name='Course Requests'),  # show all requests for the course
    path('course-students/<int:course>', StudentCourseNumberAPIView.as_view(),name='course_student'),# Students id  for each course
    path('accept-requests/<int:course>', AcceptRequest.as_view(), name='accept Requests'),  #accept array of request id's
    path('reject-requests/<int:course>', RejectRequest.as_view(), name='Reject Requests'),  #reject array of request id's

]