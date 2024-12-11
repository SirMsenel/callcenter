from django.shortcuts import render,get_object_or_404
from .models import News
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Photo,PhotoComment
from .forms import PhotoCommentForm
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from django.db.models import Count, F
from .models import Article, ArticleComment




def home(request):
   
    news_list = News.objects.all().order_by('-created_at')[:5] # Son 5 haberi alıyoruz
    article_list = Article.objects.all().order_by('-created_at')[:4]  # Son 4 makale
    most_commented_article = Article.objects.annotate(
        total_likes=Count('likes'),
        total_comments=Count('comments')
    ).order_by('-total_likes', '-total_comments', '-created_at').first()
    gallery_photos = Photo.objects.all().order_by('-uploaded_at')[:5]  # Galeri için fotoğrafları getiriyoruz (Son 5 fotoğraf)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Formu veritabanına kaydet
            contact_message = form.save()

            # Admin'e e-posta gönder
            send_mail(
                'Yeni İletişim Mesajı',
                f"Mesaj: {contact_message.message}\nAdı Soyadı: {contact_message.first_name} {contact_message.last_name}\nE-posta: {contact_message.email}\nTelefon: {contact_message.phone}",
                contact_message.email,
                [settings.ADMIN_EMAIL],  # Admin e-posta adresi
            )

            # Başarı sayfasına yönlendir
            return redirect('contact_success')  # Başarıyla gönderildikten sonra yönlendirme

    else:
        form = ContactForm()

    
    return render(request, 'news/home.html', {'news_list': news_list,
                                              'article_list' : article_list,
                                              'most_commented_article': most_commented_article,
                                              'gallery_photos': gallery_photos,
                                              'form': form})

 

def contact_success(request):
    return render(request, 'news/contact_success.html')


def search(request):
    query = request.GET.get('q')
    results = None
    if query:
        results = News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )  # Başlık veya içerik içinde arama yap
    return render(request, 'news/search_results.html', {'results': results, 'query': query})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hoş geldiniz {username}! Kayıt işleminiz tamamlandı.')
            return redirect('login')  # Kayıt olduktan sonra giriş sayfasına yönlendir
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



def news_list(request):
    all_news = News.objects.all().order_by('-created_at')  # Tüm haberler
    return render(request, 'news/news_list.html', {'all_news': all_news})


def news_detail(request, id):
    news = get_object_or_404(News, id=id)  # Haber nesnesini al
    return render(request, 'news/news_detail.html', {'news': news})



def article_list(request):
    articles = Article.objects.all().order_by('-created_at')  # Tüm haberler
    paginator = Paginator(articles, 5)  # Her sayfada 5 makale
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/article_list.html', {'articles': page_obj})


def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'news/article_detail.html', {'article': article})

@login_required
def like_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.user in article.likes.all():
        # Kullanıcı makaleyi beğenmişse, beğeniyi kaldır
        article.likes.remove(request.user)
    else:
        # Kullanıcı makaleyi beğenmemişse, beğeni ekle
        article.likes.add(request.user)
    
    # Kullanıcıyı makale detay sayfasına yönlendir
    return redirect('article_detail', id=article_id)


@login_required
def add_comment(request, article_id):  # 'id' yerine 'article_id' kullandık
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        comment_text = request.POST.get('text')
        if comment_text:
            ArticleComment.objects.create(article=article, user=request.user, text=comment_text)
    return redirect('article_detail', id=article_id)  # Yönlendirmede de 'article_id' kullanılıyor


@login_required
def delete_article_comment(request, comment_id):
    comment = get_object_or_404(ArticleComment, id=comment_id)
    
    # Yalnızca yorumu yazan kullanıcı silebilir
    if comment.user == request.user:
        comment.delete()
        return redirect('article_detail', id=comment.article.id)
    else:
        return redirect('article_detail', id=comment.article.id)


#galeri
def photo_list(request):
    photos = Photo.objects.all().order_by('-uploaded_at')  # Tarihe göre azalan sırada
    return render(request, 'news/photo_list.html', {'photos': photos})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'news/photo_detail.html', {'photo': photo})

@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)  # Beğeniyi kaldır
    else:
        photo.likes.add(request.user)  # Beğeniyi ekle
    return redirect('photo_detail', pk=pk)

# Fotoğraf yorumlarını listeleme ve yeni yorum ekleme
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    comments = photo.comments.all()  # Fotoğrafa ait tüm yorumlar
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PhotoCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.photo = photo
                comment.user = request.user
                comment.save()
                return redirect('photo_detail', pk=pk)
        else:
            return redirect('login')  # Kullanıcı giriş yapmadıysa giriş sayfasına yönlendir
    else:
        form = PhotoCommentForm()
    return render(request, 'news/photo_detail.html', {'photo': photo, 'comments': comments, 'form': form})

# Yorum silme
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(PhotoComment, id=comment_id)
    if comment.user == request.user:
        comment.delete()  # Yalnızca yorumu yapan kullanıcı silebilir
    return redirect('photo_detail', pk=comment.photo.pk)

# Hakkımızda sayfası
def about(request):
    return render(request, 'about.html')

# Kurucular sayfası
def founders(request):
    return render(request, 'founders.html')  # founders.html dosyasını oluşturun

# Hesaplama Araçları sayfası
def calculation_tools(request):
    return render(request, 'calculation_tools.html')

# Kur Takibi sayfası
def currency_tracking(request):
    return render(request, 'currency_tracking.html')

# PDF Çevirici sayfası
def pdf_converter(request):
    return render(request, 'pdf_converter.html')