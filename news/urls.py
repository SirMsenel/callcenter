from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),  # Arama URL'si
    path('', views.news_list, name='news_list'),  # Tüm haberler
    path('<int:id>/', views.news_detail, name='news_detail'),  # Haber detay
]
