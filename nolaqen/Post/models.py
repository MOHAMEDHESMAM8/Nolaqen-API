from django.db import models

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey("Courses.Courses", on_delete=models.CASCADE, db_column='course',related_name="posts_courses")
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
