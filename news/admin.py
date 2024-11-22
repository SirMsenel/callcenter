from django.contrib import admin
from .models import News, Article, Category

admin.site.register(News)

# Category modelini admin paneline ekliyoruz
admin.site.register(Category)

# Article modelini admin paneline ekliyoruz
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'published_at', 'view_count', 'comment_count')
    search_fields = ('title', 'category')  # Başlık ve kategori üzerinden arama yapılabilir
    list_filter = ('category', 'published_at')  # Kategori ve yayınlanma tarihiyle filtreleme yapılabilir