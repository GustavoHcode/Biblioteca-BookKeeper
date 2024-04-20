from django.db import models

class Reader(models.Model):
    reference_id = models.CharField(max_length=200, verbose_name="RA Aluno")
    reader_name = models.CharField(max_length=200, verbose_name="Nome do Aluno")
    reader_contact = models.CharField(max_length=200, verbose_name="Contato do Aluno")
    grade_year = models.CharField(max_length=200, verbose_name="Ano de Ensino")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.reader_name

    class Meta:
        verbose_name = "Leitor"
        verbose_name_plural = "Leitores"

class Book(models.Model):
    book_name = models.CharField(max_length=200, verbose_name="Nome do Livro")
    author = models.CharField(max_length=200, verbose_name="Autor")
    isbn = models.CharField(max_length=20, verbose_name="ISBN")
    borrowed = models.BooleanField(default=False, verbose_name="Emprestado")

    def __str__(self):
        return self.book_name

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"

