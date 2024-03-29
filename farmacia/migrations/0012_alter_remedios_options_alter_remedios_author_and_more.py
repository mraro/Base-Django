# Generated by Django 4.1.3 on 2023-03-10 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tags", "0002_remove_tag_content_type_remove_tag_object_id"),
        ("farmacia", "0011_remedios_tags"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="remedios",
            options={"verbose_name": "Medicine", "verbose_name_plural": "Medicines"},
        ),
        migrations.AlterField(
            model_name="remedios",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Author",
            ),
        ),
        migrations.AlterField(
            model_name="remedios",
            name="category",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="farmacia.category",
                verbose_name="Category",
            ),
        ),
        migrations.AlterField(
            model_name="remedios",
            name="cover",
            field=models.ImageField(
                blank=True,
                default="static/images/default.jpg",
                upload_to="farmacia/covers/%Y/%m/%d/",
                verbose_name="Cover/Image",
            ),
        ),
        migrations.AlterField(
            model_name="remedios",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
        ),
        migrations.AlterField(
            model_name="remedios",
            name="description",
            field=models.TextField(verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="remedios",
            name="is_published",
            field=models.BooleanField(default=False, verbose_name="Is Published"),
        ),
        migrations.AlterField(
            model_name="remedios",
            name="price",
            field=models.FloatField(default=1, verbose_name="Price"),
        ),
        migrations.AlterField(
            model_name="remedios",
            name="quantity",
            field=models.IntegerField(default=0, verbose_name="Quantity"),
        ),
        migrations.AlterField(
            model_name="remedios",
            name="tags",
            field=models.ManyToManyField(to="tags.tag", verbose_name="TAG"),
        ),
        migrations.AlterField(
            model_name="remedios",
            name="title",
            field=models.CharField(max_length=65, verbose_name="Title"),
        ),
        migrations.AlterField(
            model_name="remedios",
            name="update_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Update at"),
        ),
    ]
