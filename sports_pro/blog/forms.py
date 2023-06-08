from django import forms

from . import models

class BlogPostForm(forms.ModelForm):
    
    class Meta:
        models = models.BlogPostModel
        fields = "__all__"