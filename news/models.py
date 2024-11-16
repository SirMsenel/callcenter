from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)  # Haber başlığı
    content = models.TextField()  # Haber içeriği
    created_at = models.DateTimeField(auto_now_add=True)  # Oluşturulma zamanı
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)  # Haber görseli

    def __str__(self):
        return self.title

