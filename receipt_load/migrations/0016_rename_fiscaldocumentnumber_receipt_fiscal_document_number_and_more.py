# Generated by Django 4.2.4 on 2023-08-03 12:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("receipt_load", "0015_rename_store_receipt_retail"),
    ]

    operations = [
        migrations.RenameField(
            model_name="receipt",
            old_name="fiscalDocumentNumber",
            new_name="fiscal_document_number",
        ),
        migrations.RenameField(
            model_name="receipt",
            old_name="fiscalDriveNumber",
            new_name="fiscal_drive_number",
        ),
        migrations.RenameField(
            model_name="receipt",
            old_name="fiscalSign",
            new_name="fiscal_sign",
        ),
    ]
