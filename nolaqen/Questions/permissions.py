from rest_framework import permissions
from django.apps import apps

Teacher = apps.get_model('users', 'Teacher')
Student = apps.get_model('users', 'Student')
Courses = apps.get_model('Courses', 'Courses')
User = apps.get_model('users', 'User')
RejectedAccess = apps.get_model('users', 'RejectedAccess')

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_rejected_access(request, layer):
    user = request.user
    user_agent = request.META.get('HTTP_USER_AGENT')
    path = request.get_full_path_info()
    ip = visitor_ip_address(request)
    method = request.method
    obj = RejectedAccess(user=user, ip=ip, user_agent=user_agent, path=path, layer=layer,method=method)
    obj.save()


class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if Student.objects.filter(user=request.user).exists():
                if request.user.role == 'student':
                    if request.method in permissions.SAFE_METHODS:
                        return True
                else:
                    add_rejected_access(request=request, layer=1.2)
                    return False
            else:
                add_rejected_access(request=request, layer=1.1)
                return False
        else:
            return False


class StudentPost(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if (Student.objects.filter(user=request.user).exists()):
                if (request.user.role == 'student'):
                    if request.method == 'POST':
                        return True
                else:
                    add_rejected_access(request=request, layer=1.2)
                    return False
            else:
                add_rejected_access(request=request, layer=1.1)
                return False
        else:
            return False


class IsTeacher(permissions.BasePermission):
    message = 'ليس لديك الجق فى دخول هذا الصفحة'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if (Teacher.objects.filter(user=request.user).exists()):
                if (request.user.role == 'teacher'):
                    return True
                else:
                    add_rejected_access(request=request, layer=2.2)
                    return False
            else:
                add_rejected_access(request=request, layer=2.1)
                return False
        else:
            return False


class CourseOwner(permissions.BasePermission):
    message = 'انت لست المالك لهذا الكورس '

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if (Teacher.objects.filter(user=request.user).exists()):
                if (request.user.role == 'teacher'):
                    return True
                else:
                    add_rejected_access(request=request, layer=2.2)
                    return False
            else:
                add_rejected_access(request=request, layer=2.1)
                return False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.teacher.id == obj.teacher.id:
            return True
        add_rejected_access(request=request, layer=2.3)
        return False


class Owner(permissions.BasePermission):
    message = 'انت لست المالك لهذا الكورس '

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if (Teacher.objects.filter(user=request.user).exists()):
                if (request.user.role == 'teacher'):
                    return True
                else:
                    add_rejected_access(request=request, layer=2.2)
                    return False
            else:
                add_rejected_access(request=request, layer=2.1)
                return False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.teacher.id == obj.course.teacher.id:
            return True
        add_rejected_access(request=request, layer=2.3)
        return False

#  def check_owner(self,request,obj,model):
#         message = get_object_or_404(model, id=obj)
#         self.check_object_permissions(request, message)
