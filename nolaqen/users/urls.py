from django.urls import path
from .studentviews import *
from .teacherviews import *


urlpatterns = [
    path('students', StudentView.as_view(),name='students'),
    path('teachers', AllTeachers.as_view(), name='teachers'),
    path('login/', CustomTokenObtainPairView.as_view()),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
    path('news-feed/<int:course_id>', CourseNewsFeedAPIView.as_view(), name='course_newsfeed'),
    path('last_post/<int:course_id>', LastPostAPIView.as_view(), name='last_post'),
    path('last_exam/<int:course_id>', LastExamAPIView.as_view(), name='last_exam'),
    path('last_lesson/<int:course_id>', LastLessonAPIView.as_view(), name='last_lesson'),


    #teacher urls
    # path('updateTeacher/', UpdateTeacherView.as_view(), name='Update teacher'),# update teacher details (get , put)
    path('allStudentCourse/<int:course>', ALlStudentCourseView.as_view(), name='All Student Course'),# show all student for course
    path('studentInfo/<int:course>/<int:student>', StudentInfoView.as_view(), name='student info'), #get student info
    path('activateStudents/<int:course>', ActivateStudentsView.as_view(), name='activate students'),# activate list of student ids
    path('deactivateStudents/<int:course>', DeactivateStudentsView.as_view(), name='deactivate students'),# deactivate list of student ids
    path('changeGroup/<int:group>', ChangeGroupView.as_view(), name='change group '),# change group for list of student ids
    path('studentLessons/<int:course>/<int:student>', StudentAllLessonsView.as_view(), name='studentLessons'),# all lesson for student
    path('studentResults/<int:course>/<int:student>', StudentAllResultsView.as_view(), name='studentResults'),# all exam results for student
    path('lessonsBefore/<int:course>/<int:student>', LessonsBeforeStudentView.as_view(), name=' lessons before student'),# get lesson student didnt had before
    path('lessonsAddedBefore/<int:course>/<int:student>', LessonsAddedBeforeView.as_view(), name='lessons added before student '),# get lesson student had before
    path('addLessons/<int:course>/<int:student>', AddLessonsView.as_view(), name='Add lessons to student'), #add lessons to student
    # data for new group point
    # {
    #     "uncheck": [...]
    #     "check" : [..]
    # }
    path('notifications', NotificationAPIView.as_view(), name='notifications'),
    path('add_points/<int:course>', StudentPointsAPIView.as_view(), name='add_points'),
    # {
    #     "student":[1],
    #     "month_number":3
    # }
    path('student_logs/<int:month>', LogStudentAPIView.as_view(), name='student_logs'),
    path('total_month/<int:month>', MonthCountAPIView.as_view(), name='total_month'),
    path('studentLogs/<int:course>/<int:student>', StudentLogsView.as_view(), name='studentLogs'),# logs for student profile

]
 