from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('search/', views.search, name='search'),  # Arama URL'si

]
