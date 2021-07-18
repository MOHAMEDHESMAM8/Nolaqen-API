from django.urls import path
from .studentviews import *
from .teacherviews import *

urlpatterns = [
    path('exams/<int:course_id>', StudentExamAPIView.as_view(), name='exam'),
    path('my_exam/<int:exam_id>', ExamDetailsAPIView.as_view(), name='my_exam'),
    path('my_result', ExamResultAPIView.as_view(), name='my_result'),
    path('student_results', StudentResultAPIiew.as_view(), name='student_results'),
    # Teacher URL
    path('add-exam', ExamPOSTAPIView.as_view(), name='add_exam'),
    path('checkQuestions/<int:exam>', CheckedQuestionsForUpdateView.as_view(), name=' qustions'),  # checked questions for exam
    path('uncheckQuestions/<int:exam>', UncheckedQuestionsForUpdateView.as_view(), name=' qustions'),  # unchecked questions for exam
    path('addQuestions/<int:exam>', AddQuestionsForExamView.as_view(), name=' qustions'),  # unchecked questions for exam
    # data for add questions point
    #   {
    #       "uncheck": [...]
    #       "check" : [..]
    #   }
    path('questions/<int:course_id>', ExamQuestionAPIView.as_view(), name='question'),
    path('my-exams/<int:course_id>', AllExamsAPIView.as_view(), name='my_exams'),  # All Teacher Exams
    path('exam_details/<int:id>', ExamsUpdateAPIView.as_view(), name='exam_details'),  # Exam Update Delete
    path('exam_result/<int:exam_id>', AllStudentResultAPIView.as_view(), name='exam_result'),  # Students Result
    path('uncheckGroupsExam/<int:exam>', ExamUncheckedGroupsView.as_view(), name='unchecked groups'),# unchecked groups for exam
    path('checkGroupsExam/<int:exam>', LessonCheckedGroupsView.as_view(), name='checked groups'),# checked groups for exam
    path('addExamGroups/<int:exam>', AddLessonGroupsView.as_view(), name='add groups'),# add groups for exam
    # data for new group point
    #   {
    #       "uncheck": [...]
    #       "check" : [..]
    #   }
]

