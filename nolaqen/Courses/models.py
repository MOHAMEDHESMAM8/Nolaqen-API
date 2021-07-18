from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

course_dep = (
    ('علمى', 'علمى'),
    ('ادبي', 'ادبي'),
    ('الجميع', 'الجميع')
)

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey("users.Teacher", on_delete=models.CASCADE, db_column='teacher',related_name='courses_teachers')
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='courses/%y/%m/%d', null=True, blank=True)
    level = models.PositiveSmallIntegerField(validators=[
        MaxValueValidator(3),
        MinValueValidator(1)
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lesson_num = models.PositiveSmallIntegerField(default=4)
    department = models.CharField(max_length=50, choices=course_dep, blank=True, null=True)

    def __str__(self):
        return self.name


class Student_courses(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, db_column='student',related_name='student_courses_students')
    is_active = models.BooleanField(default=True)
    course = models.ForeignKey("Courses", on_delete=models.CASCADE, db_column='course',related_name='student_courses_courses')
    point = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group = models.ForeignKey("Groups.Groups", on_delete=models.CASCADE, null=True, blank=True, db_column='group',related_name='student_courses_groups')

    def __str__(self):
        return str(self.pk)

    class Meta:
        unique_together = ['course', 'student'],
        indexes = [
            models.Index(fields=['student'], name='IX_Student_courses_student'),
            models.Index(fields=['course'], name='IX_Student_courses_courses'),

        ]


class Requests(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, db_column='student',related_name='requests_students')
    course = models.ForeignKey("Courses", on_delete=models.CASCADE, db_column='course',related_name='requests_students')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['course', 'student'],
        indexes = [
            models.Index(fields=['course'], name='IX_Requests'),
        ]

    def __str__(self):
        return str(self.pk)
