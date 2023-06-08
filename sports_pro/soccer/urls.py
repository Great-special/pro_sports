from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='soccer'),
    path('live/', views.live, name='live'),
    path('favourite/', views.get_favourite, name='favourite'),
    
    path('<str:country>/<str:league>/league/fixtures/', views.league_events, name='fixturesByleague'),
    path('<str:country>/<str:league>/league/results/', views.league_events, name='resultsByleague'),
    path('<str:country>/<str:league>/league/table/', views.league_events, name='tablesByleague'),
    
    path('<str:league>/<str:stage>/fixtures/', views.competion_events, name='fixturesBycompetion'),
    path('<str:league>/<str:stage>/results/', views.competion_events, name='resultsBycompetion'),
    path('<str:league>/<str:stage>/table/', views.competion_events, name='tablesBycompetion'),
    
    path('single/<int:Eid>/', views.single_result, name='singleResult'),
    
    path('<str:eid>/', views.favourite, name='liked'),
]
