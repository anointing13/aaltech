from django.contrib import admin
from .models import News, NewsDetail


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'slug')
    search_fields = ('title', 'description')
    list_filter = ('published_date',)
    ordering = ('-published_date',)
    prepopulated_fields = {'slug': ('title',)}  # Automatically generate slug from title

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'slug')
        }),
    )

    # Exclude non-editable fields
    exclude = ('published_date',)


@admin.register(NewsDetail)
class NewsDetailAdmin(admin.ModelAdmin):
    list_display = ('news', 'full_content')
    search_fields = ('news__title', 'full_content')
    list_filter = ('news__published_date',)
    ordering = ('news__published_date',)

    fieldsets = (
        (None, {
            'fields': ('news', 'full_content')
        }),
    )
