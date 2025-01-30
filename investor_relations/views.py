from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import News, NewsDetail


def investor_relations_news(request):
    # Fetch all news items ordered by published_date
    news_items = News.objects.all().order_by('-published_date')

    # Set up pagination with 10 items per page
    paginator = Paginator(news_items, 3)
    page_number = request.GET.get('page')  # Get the current page number from the query parameters
    news_items = paginator.get_page(page_number)

    # Render the template with the paginated news items
    return render(request, 'investor_relations/news_list.html', {'news_items': news_items})


def news_detail(request, slug):
    # Fetch the details of the specific news item
    news_item = get_object_or_404(News, slug=slug)
    news_detail = get_object_or_404(NewsDetail, news=news_item)
    return render(request, 'investor_relations/news_detail.html', {'news_item': news_item, 'news_detail': news_detail})
