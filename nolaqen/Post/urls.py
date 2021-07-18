from django.urls import path
from .studentviews import *
from .teacherviews import *




urlpatterns = [
    path('posts/<int:course_id>', Postsview.as_view(), name='posts'),


    # teacher ednpoints
    path('AddPost', AddPostView.as_view(), name='Addposts'),

]