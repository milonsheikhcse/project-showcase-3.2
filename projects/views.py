from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
import time

from .models import Project
from .forms import ProjectForm
from modules.file_upload import UploadFile

def submit(request):
    if not request.user.is_authenticated:
        return redirect('user:index')

    if request.is_ajax():
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_obj = form.save(commit=False)
            project_obj.user = request.user
            project_obj.project_id = str(int(time.time()))

            upload_obj = UploadFile(request, filename='file')
            
            response = upload_obj.is_valid()
            if response:
                firebase_url = upload_obj.upload()
            else:
                return JsonResponse(response)
            
            if not firebase_url:
                return JsonResponse({
                    'status': False,
                    'msg': upload_obj.error_msg,
                })
            
            project_obj.firebase_url = firebase_url
            project_obj.save()

            return JsonResponse({
                'status': True,
                'msg': 'Successfully Uploaded Project!',
            })
        else:
            for field in form:
                print(field.errors)
            return JsonResponse({
                'status': False,
                'msg': 'Enter valid data.',
            })
   
    return render(request, 'submit.html')

def track(request):
    if not request.user.is_authenticated:
        return redirect('user:index')

    context = {
        'projects': Project.objects.filter(user=request.user).order_by('-created'),
    }
    return render(request, 'track.html', context=context)

def lists(request):
    context = {
        'projects': Project.objects.filter(status='accepted').order_by('-created'),
    }
    return render(request, 'list.html', context=context)

def details(request, pk):
    context = {
        'project': Project.objects.get(pk=pk),
    }
    return render(request, 'details.html', context=context)