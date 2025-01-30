
from django.contrib import admin
from .models import News, NewsDetail


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    search_fields = ('title', 'description')
    list_filter = ('published_date',)
    ordering = ('-published_date',)
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'slug')
        }),
    )


@admin.register(NewsDetail)
class NewsDetailAdmin(admin.ModelAdmin):
    list_display = ('news',)
    search_fields = ('news__title',)
