from django.contrib import admin
from .models import BlogPostModel, Tag
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
class PostAdmin(SummernoteModelAdmin):
    model = BlogPostModel
    summernote_fields = ('title', 'body','body2', 'body3',)
    
    list_display = (
        "id",
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    )
    list_filter = (
        "published",
        "publish_date",
    )
    list_editable = (
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    )
    search_fields = (
        "title",
        "subtitle",
        "slug",
        "body",
    )
    prepopulated_fields = {
        "slug": (
            "title",
        )
    }
    date_hierarchy = "publish_date"
    save_on_top = True
admin.site.register(BlogPostModel, PostAdmin)
