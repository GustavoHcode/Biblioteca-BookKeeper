from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model = models.StudentExtra
        fields = ['enrollment', 'branch']

        labels = {
            'enrollment': 'Registro Escolar',
            'branch': 'Ano de Ensino',
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ['name', 'isbn', 'author', 'category']

class IssuedBookForm(forms.Form):
    # O valor de to_field_name será armazenado quando o formulário for enviado
    # O método __str__ do modelo Book será mostrado na renderização HTML
    isbn2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Nome e ISBN", to_field_name="isbn", label='Nome e ISBN')
    enrollment2 = forms.ModelChoiceField(queryset=models.StudentExtra.objects.all(), empty_label="Nome e Registro Escolar", to_field_name='enrollment', label='Nome e Registro Escolar')
