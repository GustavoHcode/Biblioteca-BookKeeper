# Generated by Django 5.0.4 on 2024-04-30 19:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca_app', '0009_delete_loan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_borrowed', models.DateField(auto_now_add=True)),
                ('date_returned', models.DateField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca_app.book')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca_app.reader')),
            ],
        ),
    ]
