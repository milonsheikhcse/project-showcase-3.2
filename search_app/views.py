from django.shortcuts import render
from projects.models import Project
from functools import reduce
import operator
from django.db.models import Q

# Create your views here.
def search(request, query):
    search_list = query.split('+')
    result = Project.objects.filter(reduce(operator.or_, (Q(project_name__icontains=x) for x in search_list))).filter(status='accepted')
    context = {
        'projects': result,
        'count': len(result),
    }
    return render(request, 'search.html', context=context)