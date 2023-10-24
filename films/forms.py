from django import forms
from .models import *

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['poster', 'title_ru', 'title_orig', 'prod_year', 'timing', 'country', 'genre', 'director', 'rating']
        widgets = {
            'poster': forms.FileInput(attrs={'class': 'fieldset button button-yellow input-file form-control'}),
            'description':forms.Textarea(attrs={'rows':5})
        }
        
    def save(self, commit):
        author = settings.AUTH_USER_MODEL.objects.get(id=self.data['author_id'])
        self.instance.author = author
        return super().save(commit)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'film','text', 'date']
        widgets = {
            'description':forms.Textarea(attrs={'rows':3})
        }

class FilmSearchForm(forms.Form):
    search = forms.CharField(label='Поиск по фильмам', max_length=100)    