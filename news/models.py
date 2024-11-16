from PIL import Image
from django.db import models


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


class Article(models.Model):  # Bu satırı kontrol edin
    title = models.CharField(max_length=255)
    content = models.TextField()
    # Diğer alanlar

    def __str__(self):
        return self.title