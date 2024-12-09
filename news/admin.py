from django.contrib import admin
from .models import News, Article,ArticleComment, Category,Photo,PhotoComment
from .models import ContactMessage

admin.site.register(News)

# Category modelini admin paneline ekliyoruz
admin.site.register(Category)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'total_likes', 'total_comments')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at')

class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created_at')
    search_fields = ('text',)
    list_filter = ('created_at',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)

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


# iletişim admin.py
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'message')
    list_filter = ('created_at',)

admin.site.register(ContactMessage, ContactMessageAdmin)
