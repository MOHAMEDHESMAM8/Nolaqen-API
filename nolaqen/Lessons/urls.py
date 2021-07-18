from django.urls import path
from .studentviews import *
from .teacherviews import *


urlpatterns = [
    path('lessons/<int:course_id>', StudentLessonAPIView.as_view(), name='lesson'),
    path('views/<int:lesson>', StudentLessonViewCheck.as_view(), name='views'),

    # teacher endpoints
    path('teacher_lessons/<int:course>', AllTeacherLessons.as_view(), name='all teacher lessons'),# return all lessons for the teacher
    path('UpdateDeleteLesson/<int:lesson>', UpdateDeleteLesson.as_view(), name='UpdateDeleteLessonLesson'),# delet and edit lessons
    path('LessonViews/<int:lesson>', LessonViews.as_view(), name='AllViews'),# all views for the lesson
    path('UncheckedGroups/<int:lesson>', LessonUncheckedGroupsView.as_view(), name='uncheckedGroups'),# uncheked group for lesson
    path('checkedGroups/<int:lesson>', LessonCheckedGroupsView.as_view(), name='checkedGroups'),# cheked group for lesson
    path('addLessonGroups/<int:lesson>', AddLessonGroupsView.as_view(), name='checkedGroups'),# add  group for lesson
    # data for new group point
    # {
    #     "uncheck": [...]
    #     "check" : [..]
    # }
]
