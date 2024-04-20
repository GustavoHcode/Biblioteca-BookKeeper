from django.contrib import admin
from django.urls import path
from .views import home, save_student, readers, books, returns, save_readers, add_book

urlpatterns = [
    path('home/', home, name='home'),
    path('save/', save_student, name='save_student'),
    path('readers/', readers, name='readers'),
    path('books/', books, name='books'),
    path('returns/', returns, name='returns'),
    path('readers/add/', save_readers, name='save_readers'),
    path('books/add/', add_book, name='add_book'),
]
