from django.shortcuts import render, redirect
from django.http import JsonResponse

from projects.models import Project
from modules.file_upload import UploadFile

# done
def submissions(request):
    if not request.user.is_staff:
        return redirect('user:index')

    context = {
        'projects': Project.objects.filter(status='processing').order_by('-created'),
    }
    return render(request, 'submission.html', context=context)

# done
def all(request):
    if not request.user.is_staff:
        return redirect('user:index')

    context = {
        'projects': Project.objects.all().order_by('-created'),
    }
    return render(request, 'all.html', context=context)

# done
def accept(request, pk):
    if not request.user.is_staff:
        return redirect('user:index')

    if request.is_ajax():
        project_obj = Project.objects.get(pk=pk)
        project_obj.status = 'accepted'
        project_obj.save()
        return JsonResponse({
            'status': True,
            'msg': 'Successfully Updated Data.',
            'url': '/submissions/',
        })

# done
def reject(request, pk):
    if not request.user.is_staff:
        return redirect('user:index')

    if request.is_ajax():
        project_obj = Project.objects.get(pk=pk)
        project_obj.status = 'rejected'
        project_obj.save()

        upload_obj = UploadFile(request)
        upload_obj.delete(firebase_url=project_obj.firebase_url)

        return JsonResponse({
            'status': True,
            'msg': 'Successfully Updated Data.',
            'url': '/submissions/',
        })

# done
def delete(request, pk):
    if not request.user.is_staff:
        return redirect('user:index')

    if request.is_ajax():
        project_obj = Project.objects.get(pk=pk)

        upload_obj = UploadFile(request)
        upload_obj.delete(firebase_url=project_obj.firebase_url)

        project_obj.delete()

        return JsonResponse({
            'status': True,
            'msg': 'Successfully Updated Data.',
            'url': '/all/',
        })