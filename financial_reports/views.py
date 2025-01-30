from django.shortcuts import render, get_object_or_404
from .models import FinancialReportNews, FinancialNewsDetail
from django.core.paginator import Paginator


def financial_reports_list(request):
    news_items = FinancialReportNews.objects.all().order_by('-published_date')
    paginator = Paginator(news_items, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'financial_reports/news_list.html', {'reports': page_obj})


def financial_reports_detail(request, slug):
    news_item = get_object_or_404(FinancialReportNews, slug=slug)
    news_detail = getattr(news_item, 'details', None)  # Avoid extra database query
    return render(request, 'financial_reports/news_detail.html', {'news_item': news_item, 'news_detail': news_detail})

