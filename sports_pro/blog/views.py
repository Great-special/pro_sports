from django.shortcuts import render, get_object_or_404, redirect
from .forms import BlogPostForm
from .models import BlogPostModel

import requests
# Create your views here.


def add_blog(request):
    
    if request.method == 'POST' : # and request.FILES['image']
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_obj = form.save() 
        return redirect('/') # see_blog
    else:
        form = BlogPostForm()
 
    context = {'form': form}
    template_name = ''
    return render(request, template_name, context)


def blog_detail(request, slug):
    template_name = ''
    context = {}
    try:
        blog_obj = get_object_or_404(BlogPostModel, slug=slug)
        context['blog_obj'] = blog_obj
    except Exception as e:
        raise e
    return render(request, template_name, context)


def blog_update(request, slug):
    context = {}
    template_name = ''

    blog_obj = BlogPostModel.objects.get(slug=slug)

    initial_dict = blog_obj
    form = BlogPostForm(instance=blog_obj)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_obj)
   
        if form.is_valid():
            blog_obj = form.save()
            blog_obj.save()

            return redirect('/')
        
    context['blog_obj'] = blog_obj
    context['form'] = form
    return render(request, template_name, context)


def blog_delete(request, slug):
    blog_obj = BlogPostModel.objects.get(slug=slug)
    print(blog_obj)

    if request.user.is_authenticated:
        blog_obj.delete()

    return redirect('/')



def add_blog(request):
    
    if request.method == 'POST' : # and request.FILES['image']
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_obj = form.save() 
        return redirect('/') # see_blog
    else:
        form = BlogPostForm()
 
    context = {'form': form}
    template_name = ''
    return render(request, template_name, context)


def blog_detail(request, slug):
    template_name = ''
    context = {}
    try:
        blog_obj = get_object_or_404(BlogPostModel, slug=slug)
        context['blog_obj'] = blog_obj
    except Exception as e:
        raise e
    return render(request, template_name, context)


def news_post(request):
    template_name = 'news-left-sidebar.html'
    
    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"

    querystring = {"category":"2021020913320920836" ,"page":"1"}

    headers = {
        "X-RapidAPI-Key": "d31ffed9cdmshdd3b46d49113fffp17b050jsn36beb1a72767",
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
    
    data = response.json()
    
    context = {
        'data':data['data'],
    }
    
    return render(request, template_name, context)
    

    
def category_post(request, cat_id):
    template_name = 'news-left-sidebar.html'

    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"

    querystring = {"category":cat_id ,"page":"1"}

    headers = {
        "X-RapidAPI-Key": "d31ffed9cdmshdd3b46d49113fffp17b050jsn36beb1a72767",
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # print(response.json())
    data = response.json()
    print("......", data['data'])
    
    context = {
        'data':data['data'],
    }
    
    return render(request, template_name, context)


def detail_post(request, id):
    template_name = 'single-news.html'

    url = "https://livescore6.p.rapidapi.com/news/v2/detail"

    querystring = {"id":id}

    headers = {
        "X-RapidAPI-Key": "d31ffed9cdmshdd3b46d49113fffp17b050jsn36beb1a72767",
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
    data = response.json()
 
    context = {
        'article':data['article'],
    }
    
    return render(request, template_name, context)
    
    
