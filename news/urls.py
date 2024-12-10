from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('search/', views.search, name='search'),  # Arama URL'si
    path('news/', views.news_list, name='news_list'),  # Tüm haberler sayfası
    path('news/<int:id>/', views.news_detail, name='news_detail'),  # Haber detay sayfası
    path('articles/', views.article_list, name='articles_list'),  # Tüm makalelerin listelendiği ana sayfa
    path('articles/<int:id>/', views.article_detail, name='article_detail'),  # Makale detay sayfası
    path('articles/like/<int:article_id>/', views.like_article, name='like_article'),
    path('articles/<int:article_id>/add_comment/', views.add_comment, name='add_comment'),
    path('articles/comments/delete/<int:comment_id>/', views.delete_article_comment, name='delete_article_comment'), # Yorum silme
    path('register/', views.register, name='register'),  # Kayıt işlemi
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),  # Giriş işlemi
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Çıkış işlemi 
    path('photos/', views.photo_list, name='photo_list'),  # Fotoğraf listeleme
    path('photos/<int:pk>/', views.photo_detail, name='photo_detail'),  # Fotoğraf detay
    path('photos/<int:pk>/like/', views.like_photo, name='like_photo'),  # Beğeni
    path('photos/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),  # Yorum sil
    path('contact/success/', views.contact_success, name='contact_success'),  # Başarı mesajı sayfası
]



