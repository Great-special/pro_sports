from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.add_blog, name='add_post'),
    path('edit/', views.blog_update, name='edit_post'),
    path('detail/<str:slug>/', views.blog_detail, name='blog_detail'),
    path('delete/<str:slug>/', views.blog_delete, name='delete_post'),
    
    path('', views.news_post, name='news_post'),
    path('category/<str:cat_id>/', views.category_post, name='category_post'),
    path('<int:id>/', views.detail_post, name='detail_post'),
    
]