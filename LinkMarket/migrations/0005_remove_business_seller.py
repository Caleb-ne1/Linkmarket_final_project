# Generated by Django 5.0.4 on 2024-05-27 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("LinkMarket", "0004_category_business"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="business",
            name="seller",
        ),
    ]
