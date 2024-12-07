from django.contrib import admin
from .models import BlogPost

# Register your models here.

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'status')
    search_fields = ('title',)
    list_filter = ('status', 'published_date')
