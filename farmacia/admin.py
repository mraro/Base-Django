from django.contrib import admin

from tags.models import TAG
from .models import Category, Remedios
from django.contrib.contenttypes.admin import GenericStackedInline


# AQUI É UMA EXTENSÃO DO localhost:8000/admin OS MODELOS ADICIONADOS AQUI PODERÃO SER GERENCIADOS DIRETAMENTE POR # noqa
# USUARIO   # noqa

class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)


# UMA FORMA DE REGISTRAR AS TABELAS NO ADMIN ... # noqa
@admin.register(Remedios)
class RemediosAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'author',
                    'is_published']  # this an example way, can parse values from list, tuple or args
    list_display_links = 'id', 'title',
    list_filter = 'category', 'author', 'is_published',
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps_is_html'
    list_per_page = 20
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',)  # this copy title and make a slug text in slug field
    }
    autocomplete_fields = 'tags',
