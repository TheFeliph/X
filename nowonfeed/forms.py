# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='',  
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autofocus': True}),
        help_text='',
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmar senha',
        help_text='',  
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        # Valida se as senhas coincidem
        if password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 150:
            raise forms.ValidationError("O nome de usuário deve ter no máximo 150 caracteres.")
        return username    
    






    from django import forms
from .models import Like

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []


from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

