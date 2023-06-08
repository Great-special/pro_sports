from django.contrib import admin
from .models import FavouriteModel, IpModel
# Register your models here.
admin.site.register([FavouriteModel, IpModel])