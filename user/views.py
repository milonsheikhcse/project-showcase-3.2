from django.shortcuts import render, redirect
from django.http import JsonResponse

from modules.auth_app import RegisterObject, AuthObject

# done
def index(request):
    if request.user.is_staff:
        return redirect('admin_app:submissions')
    return render(request, 'index.html')

# done
def login(request):
    auth_obj = AuthObject(request)
    if auth_obj.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_app:submissions')
        return redirect('user:index')

    if request.is_ajax():
        auth_obj.log_in()
        return JsonResponse({
            'status': not auth_obj.error_status,
            'msg': auth_obj.msg,
            'url': '',
        })

# done
def logout(request):
    obj = AuthObject(request)
    if not obj.is_authenticated:
        return redirect('user:index')

    else:
        obj.log_out()
        return redirect('user:index')

# done
def register(request):
    register_obj = RegisterObject(request)
    if register_obj.is_authenticated:
        return redirect('user:index')
    
    if request.is_ajax():
        register_obj.create()
        return JsonResponse({
            'status': not register_obj.error_status,
            'msg': register_obj.msg,
            'url': '',
        })

# done
def guide(request):
    return render(request, 'guide.html')

# done
def contact(request):
    return render(request, 'contact.html')