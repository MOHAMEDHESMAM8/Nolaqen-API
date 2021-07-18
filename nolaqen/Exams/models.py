from django.db import models
from django.utils.translation import gettext_lazy as _


class Exams(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey("Courses.Courses", on_delete=models.CASCADE, related_name='exams_courses')
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    Limit = models.TimeField()
    description = models.CharField(max_length=255)
    color = models.CharField(max_length=25)
    lesson = lesson = models.ForeignKey("Lessons.Lessons", on_delete=models.CASCADE, db_column='lesson', null=True, blank=True,
                                        related_name='Exam_lessons')

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['course'], name='IX_Exams'),
        ]


class Exam_groups(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey("Exams", on_delete=models.CASCADE, db_column='exam',related_name='exam_groups_exams')
    group = models.ForeignKey("Groups.Groups", on_delete=models.CASCADE, db_column='group',related_name='exam_groups_groups')

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ['exam', 'group'],


class Exam_results(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey("exams", on_delete=models.CASCADE, db_column='exam',related_name='exam_results_exams')
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, db_column='student',related_name='exam_results_students')
    results = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['exam'], name='IX_Exam_results'),
        ]

    def __str__(self):
        return str(self.student)


class Exam_questions(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey("exams", on_delete=models.CASCADE, db_column='exam',related_name='question')
    question = models.ForeignKey("Questions.Questions", on_delete=models.CASCADE, db_column='question',related_name='exam_questions_questions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['exam', 'question'],
        indexes = [
            models.Index(fields=['exam'], name='IX_Exam_questions'),
        ]

    def __str__(self):
        return str(self.exam)
