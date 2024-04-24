from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Reader, Book
from .forms import BookForm

def home(request):
    return render(request, "home.html", context={"current_tab": "home"})

def readers(request):
    readers_list = Reader.objects.all()
    return render(request, "readers.html", context={"current_tab": "readers", "readers": readers_list})

def books(request):
    books_list = Book.objects.all()
    return render(request, "books.html", context={"current_tab": "books", "books": books_list})

def returns(request):
    return render(request, "returns.html", context={"current_tab": "returns"})

def multa(request):
    return HttpResponse("Consulte suas multas")

def save_student(request):
    student_name = request.POST['student_name']
    return render(request, "welcome.html", context={'student_name': student_name})

def save_readers(request):
    reader_item = Reader(
        reference_id=request.POST['reader_ref_id'],
        reader_name=request.POST['reader_name'],
        reader_contact=request.POST['reader_contact'],
        grade_year=request.POST['grade_year'],
        active=True
    )
    reader_item.save()
    return redirect('/readers')

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/books/')  # Redirecionar para a página de visualização de livros
    else:
        form = BookForm()
    
    return render(request, 'add_books.html', {'form': form, 'current_tab': 'add_book'})

