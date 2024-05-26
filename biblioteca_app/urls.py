from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from .views import home, save_student, readers, books, save_readers, add_book, remove_book, edit_book_list_view, edit_book_view, loan_books, view_loans

urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=False), name='index'),
    path('home/', home, name='home'),
    path('save/', save_student, name='save_student'),
    path('readers/', readers, name='readers'),
    path('books/', books, name='books'),
    path('readers/add/', save_readers, name='save_readers'),
    path('books/add/', add_book, name='add_book'),
    path('books/remove/', remove_book, name='remove_book'),
    path('editbook/', edit_book_list_view, name='edit_book_list'),
    path('editbook/<int:pk>/', edit_book_view, name='edit_book'),
    path('loan_books/', loan_books, name='loan_books'),
    path('returns/', view_loans, name='returns'),
]
