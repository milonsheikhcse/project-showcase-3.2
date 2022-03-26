from django.urls import path
from . import views

app_name = 'admin_app'
urlpatterns = [
    path('submissions/', views.submissions, name='submissions'),
    path('all/', views.all, name='all'),
    path('accept/?id=<int:pk>/', views.accept, name='accept'),
    path('reject/?id=<int:pk>/', views.reject, name='reject'),
    path('delete/?id=<int:pk>/', views.delete, name='delete'),
]