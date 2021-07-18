from django.urls import path
from .studentviews import *
from .teacherviews import *





urlpatterns = [
    # Student URL
    path('examquestions/<int:exam_id>' , ExamQuestionsAPIView.as_view(), name='examquestions'),
    path('wrong_answer' , WrongAnswerAPIView.as_view() , name='wrong_answer'),

    # Teacher URL
    path('question-post/<int:course_id>' , QuestionTeacherPostAPIView.as_view(), name='question_post'),
    path('question_edit/<int:id>', QuestionsUpdateAPIView.as_view(), name='question_edit'),
    # path('student_answer/<int:exam>', StudentWrongAnswersAPIView.as_view(), name='student_answer'),

]