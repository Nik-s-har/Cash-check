# Generated by Django 4.2.4 on 2023-08-03 17:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("receipt_load", "0018_сategory_parent"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Сategory",
            new_name="Category",
        ),
    ]
