from django.contrib import admin
from .models import Category, Remedios


# AQUI É UMA EXTENSÃO DO localhost:8000/admin OS MODELOS ADICIONADOS AQUI PODERÃO SER GERENCIADOS DIRETAMENTE POR USUARIO


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)

# UMA FORMA DE REGISTRAR AS TABELAS NO ADMIN ...
@admin.register(Remedios)
class RemediosAdmin(admin.ModelAdmin):
    ...
