from django.shortcuts import render, get_object_or_404
from .models import Project
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required
def construction(request):
    active_projects = Project.objects.filter(is_active=True)
    completed_projects = Project.objects.filter(is_active=False)

    # Pagination for active projects
    active_paginator = Paginator(active_projects, 3)  # 3 items per page
    active_page_number = request.GET.get('active_page', 1)
    active_page_obj = active_paginator.get_page(active_page_number)

    # Pagination for completed projects
    completed_paginator = Paginator(completed_projects, 3)  # 3 items per page
    completed_page_number = request.GET.get('completed_page', 1)
    completed_page_obj = completed_paginator.get_page(completed_page_number)

    return render(request, 'construction/construction.html', {
        'active_projects': active_page_obj,
        'completed_projects': completed_page_obj,
    })


@login_required
def residential(request):
    return render(request, 'construction/residential.html')


@login_required
def commercial(request):
    return render(request, 'construction/commercial.html')


@login_required
def civil_engineering(request):
    return render(request, 'construction/civil_engineering.html')


@login_required
def specialized(request):
    return render(request, 'construction/specialized.html')
