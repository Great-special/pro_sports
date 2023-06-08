from django.db import models

# Create your models here.
CATEGORY_CHOICES = (
    ('OV0', 'Over 0.5'),
    ('OV1', 'Over 1.5'),
    ('OV2', 'Over2')
)
CATEGORY_CHOICES2 = (
    ('OV0', 'Over 0.5'),
    ('OV1', 'Over 1.5'),
    ('OV2', 'Over2')
)

class Football(models.Model):
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    prediction = models.CharField(choices=CATEGORY_CHOICES, max_length=3)

    def __str__(self):
        return f'{self.team1} vs {self.team2}'

    # def __unicode__(self):
    #     return 
    
class Basketball(models.Model):
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    prediction = models.CharField(choices=CATEGORY_CHOICES2, max_length=3)

    def __str__(self):
        return f'{self.team1} vs {self.team2}'

    # def __unicode__(self):
    #     return 

