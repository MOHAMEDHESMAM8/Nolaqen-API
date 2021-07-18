from django.urls import path
from .studentviews import *
from .teacherviews import *

urlpatterns = [
    path('groups/<int:course>', CourseGroupsView.as_view(),name='Course Groups'),#all course Groups
    path('get-student/<int:course>', GetStudentCourses.as_view(),name='GetStudent '),#get all student with out group
    path('new-group/<int:course>', NewGroupView.as_view(), name='newGroup '),  # add group and students
    # data for new group point
    # {
    #     'name': ...
    #      "students" : [..]
    # }
    path('studentGroup/<int:group>', GetGroupStudentView.as_view(), name='studentGroup '),  # get all students for group
    path('updateGroup/<int:group>', UpdateDeleteGroupView.as_view(), name='updateGroup '),  # update group name
]

