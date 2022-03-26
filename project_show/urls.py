from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls', namespace='user')),
    path('', include('projects.urls', namespace='projects')),
    path('', include('admin_app.urls', namespace='admin_app')),
    path('', include('search_app.urls', namespace='search_app')),
]
