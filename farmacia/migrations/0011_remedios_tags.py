# Generated by Django 4.1.3 on 2023-03-07 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tags", "0002_remove_tag_content_type_remove_tag_object_id"),
        ("farmacia", "0010_alter_remedios_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="remedios",
            name="tags",
            field=models.ManyToManyField(to="tags.tag"),
        ),
    ]
