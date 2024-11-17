from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('search/', views.search, name='search'),  # Arama URL'si
    path('', views.news_list, name='news_list'),  # Tüm haberler
    path('<int:id>/', views.news_detail, name='news_detail'),  # Haber detay
    path('articles/', views.article_list, name='articles_list'),
    path('register/', views.register, name='register'), #kayıt sistemi
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),  # Giriş işlemi
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Çıkış işlemi 
]


# urls.py
from django.conf import settings
from django.conf.urls.static import static
# Eğer proje geliştirme aşamasında ise
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)