from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PhotoComment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,  # Kullanıcı adı alanındaki yardımcı metni kaldırır
            'email': None,     # E-posta alanındaki yardımcı metni kaldırır
            'password1': None, # Şifre alanındaki yardımcı metni kaldırır
            'password2': None, # Şifre doğrulama alanındaki yardımcı metni kaldırır
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Burada kullanıcı adı için özelleştirilmiş doğrulama ekleyebilirsiniz
        return username
    
class PhotoCommentForm(forms.ModelForm):
    class Meta:
        model = PhotoComment
        fields = ['text']  # Kullanıcı yalnızca yorum metnini girebilir
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Yorum yazın...'}),
        }