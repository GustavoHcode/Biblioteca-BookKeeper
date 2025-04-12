from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Reader, Book, Loan
from .forms import BookForm, ContactForm
from .models import Book
from datetime import datetime, timedelta
from django.contrib import messages 
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.loader import render_to_string
from bs4 import BeautifulSoup
from xhtml2pdf import pisa
from weasyprint import HTML
from .models import Book, Loan 
import os


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

        loan = Loan.objects.create(book=book, reader=reader, date_borrowed=date_borrowed, date_returned=date_borrowed)

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



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['Nome']
            email = form.cleaned_data['Email']
            message = form.cleaned_data['Mensagem']

            try:
                # Envio do e-mail
                EmailMessage(
                    subject='Contact Form Submission from {}'.format(name),
                    body=message,
                    from_email='sandbox.smtp.mailtrap.io',  
                    to=['sandbox.smtp.mailtrap.io'],  
                    reply_to=[email]
                ).send()

                return redirect('success')

            except Exception as e:
                print(f'Error sending email: {e}')  
                return render(request, 'contact.html', {'form': form, 'error': 'Falha ao enviar e-mail. Por favor, tente novamente.'})

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def success(request):
    return HttpResponse('Seu problema foi enviado com sucesso!')



def relatorio(request):
    livros = Book.objects.all() 
    loans = Loan.objects.all()
    return render(request, 'relatorio.html', {'books': livros, 'loans': loans})
  
    
def gerar_pdf(request):
    books = Book.objects.all()
    loans = Loan.objects.all()

    html_string = render_to_string("relatorio.html", {"books": books, "loans": loans})

    
    soup = BeautifulSoup(html_string, "html.parser")
    conteudo_pdf = soup.find(id="conteudo-pdf")
   
    pdf = HTML(string=str(conteudo_pdf)).write_pdf()

    
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="relatorio.pdf"'
    return response