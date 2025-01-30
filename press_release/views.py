from django.shortcuts import render, get_object_or_404
from .models import News, NewsDetail
from django.core.paginator import Paginator


def press_release_list(request):
    news_items = News.objects.all().order_by('-published_date')  # Fetch the news articles
    paginator = Paginator(news_items, 3)  # Show 3 articles per page (you can change this number)
    page_number = request.GET.get('page')  # Get the page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page
    return render(request, 'press_release/news_list.html', {'reports': page_obj})


def press_release_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    news_detail = get_object_or_404(NewsDetail, news=news_item)  # Get related NewsDetail
    return render(request, 'press_release/news_detail.html', {'news_item': news_item, 'news_detail': news_detail})
