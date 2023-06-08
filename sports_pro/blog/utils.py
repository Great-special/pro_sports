from django.utils.text import slugify

from . import models

import string
import random


def generate_random_string(Num):
    res = "-".join(random.choices(string.ascii_uppercase + string.digits, k = Num))
    return res


def generate_slug(text):
    
    gen_slug = slugify(text)
    
    if models.BlogPostModel.objects.filter(slug = gen_slug).exists():
       gen_slug = gen_slug + generate_random_string(5)
        
    return gen_slug