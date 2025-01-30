from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Events

def event_list(request):
    events = Events.objects.all().order_by('-published_date')
    paginator = Paginator(events, 3)  # 3 events per page
    page_number = request.GET.get('page')
    reports = paginator.get_page(page_number)
    return render(request, 'events/event_list.html', {'reports': reports})

def event_detail(request, slug):
    event = get_object_or_404(Events, slug=slug)
    return render(request, 'events/event_detail.html', {'event': event})
