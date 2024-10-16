from django import forms
from .models import Book
from django.core.validators import EmailValidator

# Formulário para o modelo Book
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_name', 'author', 'isbn']

class ContactForm(forms.Form):
    Nome = forms.CharField(max_length=100)
    Email = forms.CharField(validators=[EmailValidator()])
    Celular = forms.CharField(max_length=15)
    Assunto = forms.CharField(max_length=100)
    Mensagem = forms.CharField(widget=forms.Textarea)