# Generated by Django 4.1.3 on 2023-01-10 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farmacia", "0007_alter_remedios_cover"),
    ]

    operations = [
        migrations.AlterField(
            model_name="remedios", name="slug", field=models.SlugField(unique=True),
        ),
    ]