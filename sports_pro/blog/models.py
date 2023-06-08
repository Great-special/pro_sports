from django.db import models
from django.conf import settings
from .utils import generate_slug
from django.utils import timezone

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name

class BlogPostModel(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to='blog-images', null=True, blank=True)
    body2 = models.TextField(null=True, blank=True)
    image2 = models.ImageField(upload_to='blog-images', null=True, blank=True)
    body3 = models.TextField(null=True, blank=True)
    image3 = models.ImageField(upload_to='blog-images', null=True, blank=True)
    video = models.FileField(upload_to='blog-videos', null=True, blank=True)
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    # author = models.ForeignKey(User, on_delete=models.PROTECT)
    
    class Meta:
        ordering = ["-publish_date"]
        
    def __str__(self):
        return self.title[0:50]
    
    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("blog-post", kwargs={"slug": self.slug})
    
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(BlogPostModel, self).save(*args, **kwargs)
    
   
    def get_image_url(self):
        image_url = self.image.url
        return image_url

    
