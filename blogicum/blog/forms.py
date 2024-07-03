from django import forms

from .models import Post, Comment, User


class PostForm(forms.ModelForm):
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Post
        # Указываем, что надо отобразить все поля.
        exclude = ('author',)

        widgets = {
            'pub_date': forms.DateInput(
                format='%Y-%m-%d %H:%M', attrs={'type': 'datetime-local'}
            )
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
