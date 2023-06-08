from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='basketball'),
    path('live/', views.live, name='basketball_live'),
    
    path('<str:country>/<str:league>/league/fixtures/', views.league_events, name='basketball_fixturesByleague'),
    path('<str:country>/<str:league>/league/results/', views.league_events, name='basketball_resultsByleague'),
    path('<str:country>/<str:league>/league/table/', views.league_events, name='basketball_tablesByleague'),
    
    path('single/<int:Eid>/', views.single_result, name='basketball_singleResult'),
]
