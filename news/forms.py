from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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