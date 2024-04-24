from django.contrib import admin
from .models import Reader, Book

# Register your models here.
admin.site.register(Reader)

class BookAdmin(admin.ModelAdmin):
    list_display = ['book_name', 'author', 'isbn', 'borrowed']

admin.site.register(Book, BookAdmin)
