from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['created', 'updated', 'firebase_url', 'user', 'project_id', 'status']