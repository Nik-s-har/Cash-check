# Generated by Django 4.2.4 on 2023-08-03 12:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("receipt_load", "0012_rename_keywords_сategory_tags"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Store_receipt",
            new_name="Receipt",
        ),
    ]
