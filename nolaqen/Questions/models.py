from re import S
from django.db import models
from django.utils.translation import gettext_lazy as _


class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey("Courses.Courses", on_delete=models.CASCADE, db_column='course',related_name="questions_courses")
    isMultiple = models.BooleanField()
    isTrueFalse = models.BooleanField()
    content = models.CharField(max_length=455)
    degree = models.PositiveSmallIntegerField()
    photo = models.ImageField(upload_to='questions/%y/%m/%d' , blank=True , null=True)
    class Meta:
        indexes = [
            models.Index(fields=['course'], name='IX_Questions'),
        ]

    def __str__(self):
        return str(self.id)


class Question_answers(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey("Questions", null=True, on_delete=models.CASCADE, db_column='question' , related_name='answer')
    is_correct = models.BooleanField(default=False)
    answer = models.CharField(max_length=70)

    class Meta:
        indexes = [
            models.Index(fields=['question'], name='IX_Question_answers'),
        ]

    def __str__(self):
        return str(self.id)


class Wrong_answers(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, db_column='student',related_name='wrong_answers_students')
    question = models.ForeignKey("Questions", on_delete=models.CASCADE, db_column='question',related_name='wrong_answers_questions')
    selected_answer = models.ForeignKey("Question_answers", on_delete=models.CASCADE, db_column='selected_answer',related_name='wrong_answers_selected_answer')

    class Meta:
        unique_together = ['student', 'question'],
        indexes = [
            models.Index(fields=['question'], name='IX_wrong_answers'),
        ]

    def __str__(self):
        return str(self.id)
