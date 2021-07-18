from django.db import models



class Groups(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    course = models.ForeignKey("Courses.Courses", on_delete=models.CASCADE,related_name='groups_courses')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
