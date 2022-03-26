from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    # path('projects/', views.projects, name='projects'),
    path('guide/', views.guide, name='guide'),
    path('contact/', views.contact, name='contact'),
]