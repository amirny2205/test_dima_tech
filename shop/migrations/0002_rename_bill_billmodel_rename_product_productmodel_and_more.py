# Generated by Django 4.1.2 on 2022-10-22 18:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bill',
            new_name='BillModel',
        ),
        migrations.RenameModel(
            old_name='Product',
            new_name='ProductModel',
        ),
        migrations.RenameModel(
            old_name='Transaction',
            new_name='TransactionModel',
        ),
    ]
