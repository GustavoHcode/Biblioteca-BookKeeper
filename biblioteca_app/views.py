from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Reader, Book, Loan
from .forms import BookForm
from .models import Book
from datetime import datetime, timedelta
from django.contrib import messages


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


# remove books

def remove_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        if book_id:
            try:
                book_to_delete = Book.objects.get(id=book_id)
                book_to_delete.delete()
                return redirect('books')  
            except Book.DoesNotExist:
                pass  
    books_list = Book.objects.all()
    return render(request, "remove_books.html", context={"current_tab": "remove_book", "books": books_list})

# Edit book

def edit_book_list_view(request):
    books = Book.objects.all()
    return render(request, 'edit_book_list.html', {'books': books})

def edit_book_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('books'))
    else:
        form = BookForm(instance=book)
    
    return render(request, 'editbook.html', {'form': form})

#Emprestimo de livros
def loan_books(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        reader_id = request.POST.get('reader')
        days = request.POST.get('days')

        if not all([book_id, reader_id, days]):
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('loan_books')

        try:
            book = Book.objects.get(pk=book_id)
            reader = Reader.objects.get(pk=reader_id)
            days = int(days)
        except (ValueError, Book.DoesNotExist, Reader.DoesNotExist):
            messages.error(request, 'Livro ou leitor inválido.')
            return redirect('loan_books')

        if Loan.objects.filter(book=book, date_returned=None).exists():
            messages.error(request, 'Este livro já está emprestado.')
            return redirect('loan_books')

        date_borrowed = datetime.now().date()
        date_returned = date_borrowed + timedelta(days=days)

        loan = Loan.objects.create(book=book, reader=reader, date_borrowed=date_borrowed, date_returned=date_returned)

        messages.success(request, 'Empréstimo realizado com sucesso.')
        return redirect('loan_books')

    else:
        # Passando os livros e leitores para o template
        books = Book.objects.all()
        readers = Reader.objects.all()
        return render(request, 'loan_books.html', {'books': books, 'readers': readers})
    

    #lista de emprestimos 
def view_loans(request):
    print("Acessando a view view_loans")
    loans = Loan.objects.all()
    print("Empréstimos recuperados:", loans)
    return render(request, 'returns.html', {'loans': loans})