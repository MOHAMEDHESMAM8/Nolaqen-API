from django.apps import apps
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *

Student_courses = apps.get_model('Courses', 'Student_courses')
Groups = apps.get_model('Groups', 'Groups')
Lesson_views = apps.get_model('Lessons', 'Lesson_views')
Lessons = apps.get_model('Lessons', 'Lessons')
Exam_results = apps.get_model('Exams', 'Exam_results')
Exams = apps.get_model('Exams', 'Exams')
Courses = apps.get_model('Courses', 'Courses')
Student_lessons = apps.get_model('Lessons', 'Student_lessons')
Posts = apps.get_model('Post', 'Posts')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['role'] = user.role
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'password', 'first_name', 'last_name', 'email', ]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class RegisterUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ('user', 'level', 'department', 'parent_phone')

    def to_representation(self, instance):
        data = super(RegisterUserSerializer, self).to_representation(instance)
        User = data.pop('user')
        for key, val in User.items():
            data.update({key: val})
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student, created = Student.objects.update_or_create(user=user, level=validated_data.pop('level'),
                                                            department=validated_data.pop('department'),
                                                            parent_phone=validated_data.pop('parent_phone'),
                                                            )
        return student


class UserTeacherViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class TeachersViewSerializer(serializers.ModelSerializer):
    user = UserTeacherViewSerializer()

    class Meta:
        model = Teacher
        fields = ('user', 'photo')

    def to_representation(self, instance):
        data = super(TeachersViewSerializer, self).to_representation(instance)
        teacher = data.pop('user')
        for key, val in teacher.items():
            data.update({key: val})
        return data


class ALlUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', ]


class ALlStudentSerializer(serializers.ModelSerializer):
    user = ALlUserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'parent_phone', 'user', 'department']

    def to_representation(self, instance):
        data = super(ALlStudentSerializer, self).to_representation(instance)
        user = data.pop('user')
        for key, val in user.items():
            data.update({key: val})
        return data


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['name']


class ALlStudentCourseSerializer(serializers.ModelSerializer):
    student = ALlStudentSerializer()
    group = StudentGroupSerializer()

    class Meta:
        model = Student_courses
        fields = ['student', 'point', 'is_active', 'group']

    def to_representation(self, instance):
        data = super(ALlStudentCourseSerializer, self).to_representation(instance)
        student = data.pop('student')
        for key, val in student.items():
            data.update({key: val})
        return data



class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['id', 'name']


class ALlLessonsSerializer(serializers.ModelSerializer):
    lesson = LessonsSerializer()

    class Meta:
        model = Lesson_views
        fields = ['lesson', 'created_at']

    def to_representation(self, instance):
        data = super(ALlLessonsSerializer, self).to_representation(instance)
        lesson = data.pop('lesson')
        for key, val in lesson.items():
            data.update({key: val})
        return data


class ExamDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exams
        fields = ['name']


class AllStudentResults(serializers.ModelSerializer):
    exam = ExamDetailsSerializer()

    class Meta:
        model = Exam_results
        fields = ['exam', 'results', 'created_at']

    def to_representation(self, instance):
        data = super(AllStudentResults, self).to_representation(instance)
        exam = data.pop('exam')
        for key, val in exam.items():
            data.update({key: val})
        return data


class LessonsBeforeStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['name', 'id', 'description']


class AddedLessonsSerializer(serializers.ModelSerializer):
    lesson = LessonsBeforeStudentSerializer()

    class Meta:
        model = Student_courses
        fields = ['lesson']

    def to_representation(self, instance):
        data = super(AddedLessonsSerializer, self).to_representation(instance)
        lesson = data.pop('lesson')
        for key, val in lesson.items():
            data.update({key: val})
        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['created_at', 'viewed', 'message']


class StudentUserSerializer(serializers.ModelSerializer):
    user = UserTeacherViewSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user']

    def to_representation(self, instance):
        data = super(StudentUserSerializer, self).to_representation(instance)
        lesson = data.pop('user')
        for key, val in lesson.items():
            data.update({key: val})
        return data


class logsCouresNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['name']


class LogsStudentSerializer(serializers.ModelSerializer):
    student = StudentUserSerializer()
    course = logsCouresNameSerializer()

    class Meta:
        model = Logs
        fields = ['student', 'course', 'month_number']

    def to_representation(self, instance):
        data = super(LogsStudentSerializer, self).to_representation(instance)
        student = data.pop('student')
        course = data.pop('course')
        for key, val in student.items():
            data.update({key: val})
        for key, val in course.items():
            data.update({key: val})
        return data





class  StudentLogsProfile(serializers.ModelSerializer):
    
    class Meta:
        model = Logs 
        fields = ["month_number","created_at"]
# what is this for
# class TeacherCourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Courses
#         fields = ['name', 'level']
# 
# 
# class TeacherLogsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Logs
#         fields = ['course']


class StudentTeacherDataSerializer(serializers.ModelSerializer):
    user = ALlUserSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'photo']

    def to_representation(self, instance):
        data = super(StudentTeacherDataSerializer, self).to_representation(instance)
        user = data.pop('user')
        for key, val in user.items():
            data.update({key: val})
        return data

class StudentCourseDataSerializer(serializers.ModelSerializer):
    teacher = StudentTeacherDataSerializer()

    class Meta:
        model = Courses
        fields = ['teacher', 'photo']

    def to_representation(self, instance):
        data = super(StudentCourseDataSerializer, self).to_representation(instance)
        teacher = data.pop('teacher')
        teacher['teacher_photo'] = teacher.pop('photo')
        for key, val in teacher.items():
            data.update({key: val})
        return data

class LastPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['content']

class LastExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exams
        fields = ['name', 'created_at', 'end_at']
        
class LastLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['name', 'description', 'created_at']