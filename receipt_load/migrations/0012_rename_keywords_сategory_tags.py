# Generated by Django 4.2.4 on 2023-08-03 12:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("receipt_load", "0011_rename_categoryname_сategory_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="сategory",
            old_name="keyWords",
            new_name="tags",
        ),
    ]
