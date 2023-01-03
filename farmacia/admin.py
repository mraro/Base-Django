from django.contrib import admin
from .models import Category, Farmacia


# AQUI É UMA EXTENSÃO DO localhost:8000/admin OS MODELOS ADICIONADOS AQUI PODERÃO SER GERENCIADOS DIRETAMENTE POR USUARIO

# UMA FORMA DE REGISTRAR AS TABELAS NO ADMIN ...

class CategoryAdmin(admin.ModelAdmin):
    ...
@admin.register(Farmacia)
class FarmaciaAdmin(admin.ModelAdmin):
    ...
admin.site.register(Category, CategoryAdmin)
