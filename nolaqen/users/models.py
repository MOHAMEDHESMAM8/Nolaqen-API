from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver




user_role = (
    ('admin', "admin"),
    ('teacher', "teacher"),
    ('student', "student"),
    ('parent', "parent")
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The given phone must be set')
        self.phone = phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    phone_regex = RegexValidator(regex=r'^(010|011|012|015)',
                                 message="رقم الهاتف يجب ان يبدا ب 011 او 012 او 010 او 015 و يجب ان يكون مكون من 11 رقم")
    phone = models.CharField(validators=[
        RegexValidator('^(010|011|012|015)[0-9]{8}$',
                       message='رقم الهاتف يجب ان يبدا ب 011 او 012 او 010 او 015 و يجب ان يكون مكون من 11 رقم',

                       ), ], max_length=11, unique=True)
    username = None
    role = models.CharField(default='student', max_length=19, choices=user_role)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user',related_name='student')
    level = models.PositiveSmallIntegerField(validators=[
        MaxValueValidator(3),
        MinValueValidator(1)
    ])
    department = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^(010|011|012|015)',
                                 message="رقم الهاتف يجب ان يبدا ب 011 او 012 او 010 او 015 و يجب ان يكون مكون من 11 رقم")
    parent_phone = models.CharField(validators=[
        RegexValidator('^(010|011|012|015)[0-9]{8}$',
                       message='رقم الهاتف يجب ان يبدا ب 011 او 012 او 010 او 015 و يجب ان يكون مكون من 11 رقم',
                       ), ], max_length=11)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user',related_name='admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user',related_name='teacher')
    subject = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='teachers/%y/%m/%d', null=True, blank=True)
    cover = models.ImageField(upload_to='teachers/%y/%m/%d', null=True, blank=True)
    offline_system = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Parents_user(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE,related_name='parents_user')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.user.first_name + ' ' + self.student.user.last_name


class StudentIp(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE,related_name='student_ip')
    ip = models.IntegerField()
    user_Agent = models.CharField(max_length=255)

    def __str__(self):
        return self.student.user.first_name + ' ' + self.student.user.last_name


class RejectedAccess(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=15)
    user_agent = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user', related_name='Rejected_access_user')
    path = models.TextField()
    layer = models.CharField(max_length=3,default=0)
    method = models.CharField(max_length=10,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     if instance.role == 'admin':
#         instance.admin.save()
#     if instance.role == 'teacher':
#         instance.teacher.save()
#     if instance.role == 'student':
#         instance.student.save()

class Logs(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='logs_student')
    course = models.ForeignKey("Courses.Courses", on_delete=models.CASCADE, related_name='logs_courses')
    month_number = models.PositiveSmallIntegerField(validators=[
        MaxValueValidator(3),
        MinValueValidator(1)
    ])
    created_at = models.DateField(auto_now_add=True)

    def str(self):
        return str(self.course)

class Notification(models.Model):
    NOTIFICATION_TYPE = ((1, 'Accepted Request'), (2, 'Rejected Request'), (3, 'Post'), (4, 'Exam'), (5, "Lesson"))
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_column='teacher')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student', null=True)
    course = models.ForeignKey('Courses.Courses', on_delete=models.CASCADE, db_column='course')
    group = models.ForeignKey('Groups.Groups', on_delete=models.CASCADE, null=True, db_column='group')
    message = models.CharField(max_length=255, null=True)
    type = models.IntegerField(choices=NOTIFICATION_TYPE)
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)