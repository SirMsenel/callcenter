from PIL import Image
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(default="Bu haberin özeti henüz eklenmemiştir.")
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)

            # Görseli yeniden boyutlandır
            max_size = (800, 400)  # Maksimum genişlik ve yükseklik
            img.thumbnail(max_size, Image.Resampling.LANCZOS)  # Yeni yöntem
            img.save(self.image.path)


# Category modelini elle girilebilir şekilde bırakıyoruz
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Article modelini güncelliyoruz
class Article(models.Model):
    title = models.CharField(max_length=200)  # Makale başlığı
    summary = models.TextField()  # Makale özeti
    content = models.TextField()  # Makale içeriği
    image = models.ImageField(upload_to='article/', null=True, blank=True)  # Image alanı, media/news_images klasörüne kaydedilecek
    category = models.CharField(max_length=100, null=True, blank=True)  # null=True ve blank=True ile boş bırakılabilir
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # null=True olarak güncellendi
    published_at = models.DateTimeField(null=True, blank=True)  # Kullanıcıya tarih seçme imkanı
    view_count = models.IntegerField(default=0)  # Görüntülenme sayısı
    comment_count = models.IntegerField(default=0)  # Yorum sayısı

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


#Fotoğraf Modeli
class Photo(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)  # Fotoğraf başlığı (isteğe bağlı)
    image = models.ImageField(upload_to='photos/')  # Fotoğraf dosyası
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Yüklenme tarihi
    likes = models.ManyToManyField('auth.User', related_name='liked_photos', blank=True)  # Beğeniler

    def __str__(self):
        return self.title or f"Photo {self.id}"

    def total_likes(self):
        return self.likes.count()

# Fotoğraf Yorum Modeli
class PhotoComment(models.Model):
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, related_name='comments')  # Fotoğraf ile ilişki
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Yorum yapan kullanıcı
    text = models.TextField()  # Yorum içeriği
    created_at = models.DateTimeField(auto_now_add=True)  # Yorumun oluşturulma zamanı

    def __str__(self):
        return f"Comment by {self.user.username} on {self.photo}"
