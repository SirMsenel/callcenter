from django.contrib import admin
from .models import News, Article, Category,Photo,PhotoComment

admin.site.register(News)

# Category modelini admin paneline ekliyoruz
admin.site.register(Category)

# Article modelini admin paneline ekliyoruz
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'published_at', 'view_count', 'comment_count')
    search_fields = ('title', 'category')  # Başlık ve kategori üzerinden arama yapılabilir
    list_filter = ('category', 'published_at')  # Kategori ve yayınlanma tarihiyle filtreleme yapılabilir

# Photo(galeri) modelini admin paneline ekliyoruz
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'total_likes')  # Görüntülenecek sütunlar
    search_fields = ('title',)  # Başlık üzerinden arama yapılabilir
    list_filter = ('uploaded_at',)  # Yükleme tarihi filtrelenebilir

#Photo için Comment(yorum) modelini panele ekliyoruz
@admin.register(PhotoComment)
class PhotoCommentAdmin(admin.ModelAdmin):
    list_display = ('photo', 'user', 'created_at')
    search_fields = ('user__username', 'photo__title', 'text')
    list_filter = ('created_at',)
