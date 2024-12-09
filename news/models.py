from PIL import Image
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timezone import now


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


# Makale Modeli
class Article(models.Model):
    title = models.CharField(max_length=200)  # Makale başlığı
    summary = models.TextField()  # Makale özeti
    content = models.TextField()  # Makale içeriği
    image = models.ImageField(upload_to='articles/', null=True, blank=True)  # Makale görseli
    category = models.CharField(max_length=100, null=True, blank=True)  # Makale kategorisi
    created_at = models.DateTimeField(auto_now_add=True)  # Yorumun oluşturulma tarihi
    published_at = models.DateTimeField(null=True, blank=True)  # Yayınlanma tarihi
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True)  # Beğeniler

    def __str__(self):
        return self.title

    def total_likes(self):
        """Makale için toplam beğeni sayısını döndürür."""
        return self.likes.count()

    def total_comments(self):
        """Makale için toplam yorum sayısını döndürür."""
        return self.comments.count()


# Makale Yorum Modeli
class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')  # Makale ile ilişki
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Yorumu yapan kullanıcı
    text = models.TextField()  # Yorum içeriği
    created_at = models.DateTimeField(auto_now_add=True)  # Yorumun oluşturulma tarihi

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article}"


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
    
    def total_comments(self):
        return self.comments.count()  # İlgili yorumları sayar


# Fotoğraf Yorum Modeli
class PhotoComment(models.Model):
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, related_name='comments')  # Fotoğraf ile ilişki
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Yorum yapan kullanıcı
    text = models.TextField()  # Yorum içeriği
    created_at = models.DateTimeField(auto_now_add=True)  # Yorumun oluşturulma zamanı

    def __str__(self):
        return f"Comment by {self.user.username} on {self.photo}"


# iletişim modeli
class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ad")
    last_name = models.CharField(max_length=100, verbose_name="Soyad")
    email = models.EmailField(verbose_name="E-posta")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon Numarası")
    message = models.TextField(verbose_name="Mesaj")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Mesaj Tarihi")

    def __str__(self):
        return f"Mesaj: {self.first_name} {self.last_name} - {self.email}"

    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
