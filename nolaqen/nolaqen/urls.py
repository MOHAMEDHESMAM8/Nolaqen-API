from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api-auth',include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/lessons/', include('Lessons.urls')),
    path('api/exams/', include('Exams.urls')),
    path('api/groups/', include('Groups.urls')),
    path('api/questions/', include('Questions.urls')),
    path('api/courses/', include('Courses.urls')),
    path('api/posts/', include('Post.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

