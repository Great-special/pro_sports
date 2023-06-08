
from django.db import models
from django.contrib.auth.models import User

class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class FavouriteModel(models.Model):
    Eid = models.IntegerField()
    owner = models.ManyToManyField(IpModel, related_name="favourite_owner", blank=True)

    def __str__(self):
        return str(self.Eid)

    def total_owned(self):
        return self.owner.count()