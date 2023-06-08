from django.contrib import admin
from .models import Football, Basketball
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    model = Football
    summernote_fields = ('team1', 'team2',)
    
    list_display = (
        "id",
        "team1",
        "team2",
        "prediction",
        
    )
    list_filter = (
        "prediction",
    )
    list_editable = (
        "team1",
        "team2",
        "prediction",
    )
    # search_fields = (
    #     "title",
    #     "subtitle",
    #     "slug",
    #     "body",
    # )
    # prepopulated_fields = {
    #     "slug": (
    #         "title",
    #     )
    # }
    # date_hierarchy = ""
    save_on_top = True
admin.site.register(Football, PostAdmin)

class PostAdmin(SummernoteModelAdmin):
    model = Basketball
    summernote_fields = ('team1', 'team2',)
    
    list_display = (
        "id",
        "team1",
        "team2",
        "prediction",
        
    )
    list_filter = (
        "prediction",
    )
    list_editable = (
        "team1",
        "team2",
        "prediction",
    )
    # search_fields = (
    #     "title",
    #     "subtitle",
    #     "slug",
    #     "body",
    # )
    # prepopulated_fields = {
    #     "slug": (
    #         "title",
    #     )
    # }
    # date_hierarchy = ""
    save_on_top = True
admin.site.register(Basketball, PostAdmin)
