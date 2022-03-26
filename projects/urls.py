from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('submit/', views.submit, name='submit'),
    path('track/', views.track, name='track'),
    path('lists/', views.lists, name='lists'),
    path('details/?id=<int:pk>/', views.details, name='details'),
]