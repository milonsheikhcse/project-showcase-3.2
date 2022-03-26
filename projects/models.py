from django.db import models
from django.contrib.auth.models import User

from user.models import Profile

# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    project_id = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    institute = models.CharField(max_length=255)
    keywords = models.TextField()
    firebase_url = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, default='processing')

    def __str__(self):
        return self.project_name

    @property
    def created_by(self):
        profile = Profile.objects.get(user=self.user)
        return (profile.first_name + ' ' + profile.last_name).title()

    @property
    def id_no(self):
        profile = Profile.objects.get(user=self.user)
        return profile.id_no

    @property
    def session(self):
        profile = Profile.objects.get(user=self.user)
        return profile.session