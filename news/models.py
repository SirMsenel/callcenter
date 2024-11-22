from PIL import Image
from django.db import models
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(default="Bu haberin özeti henüz eklenmemiştir.")
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    created_at = models.DateTimeField(auto_now_add=True)


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