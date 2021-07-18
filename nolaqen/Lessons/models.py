from django.db import models


class  views(models.Model):
    views = models.BooleanField(default=False)
    single_view =models.PositiveSmallIntegerField(default=6)


class Lessons(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey("Courses.Courses", on_delete=models.CASCADE,db_column='course',related_name='lessons_courses')
    name = models.CharField(max_length=50)
    source = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['course'], name='IX_lessons'),
        ]

    def __str__(self):
        return self.name


class Lesson_views(models.Model):
    id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey("Lessons", on_delete=models.CASCADE,db_column='lesson',related_name='lesson_views_lessons')
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE,db_column='student',related_name='lesson_views_students')
    views = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lesson.name

    class Meta:
        unique_together = ['lesson', 'student'],
        indexes = [
            models.Index(fields=['lesson', 'student'], name='IX_Lesson_views'),
        ]


class Lesson_groups(models.Model):
    id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey("Lessons", on_delete=models.CASCADE,db_column='lesson',related_name='lesson_groups_lessons')
    group = models.ForeignKey("Groups.Groups", on_delete=models.CASCADE,db_column='group',related_name='lesson_groups_groups')

    def __str__(self):
        return str(self.pk)

    class Meta:
        unique_together = ['lesson', 'group'],
        indexes = [
            models.Index(fields=['group'], name='IX_Lesson_groups'),
        ]


class Student_lessons(models.Model):
    id =models.AutoField(primary_key=True)
    lesson = models.ForeignKey("Lessons", on_delete=models.CASCADE, db_column='lesson',
                               related_name='Student_lessons_lessons')
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, db_column='student',
                                related_name='Student_lessons_students')

    class Meta:
        unique_together = ['lesson', 'student'],
        indexes = [
            models.Index(fields=['student'], name='IX_Student_lessons'),
        ]

