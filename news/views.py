from django.shortcuts import render, get_object_or_404
from .models import News, NewsDetail
from django.core.paginator import Paginator


# View for the news list
def news_list(request):
    news_items = News.objects.all().order_by('-published_date')  # Get all news, ordered by published date
    paginator = Paginator(news_items, 3)  # Show 3 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news_list.html', {'news_items': page_obj})


# View for individual news detail
def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)  # Get the news article by slug
    news_detail = get_object_or_404(NewsDetail, news=news_item)  # Get the related news detail
    return render(request, 'news/news_detail.html',
                  {'news_item': news_item, 'news_detail': news_detail, 'full_content': news_detail.full_content})
