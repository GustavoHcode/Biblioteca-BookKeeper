# Generated by Django 5.0.4 on 2024-04-16 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca_app', '0006_loan'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Loan',
        ),
    ]