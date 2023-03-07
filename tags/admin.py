from django.contrib import admin

from tags.models import TAG


# Register your models here.
@admin.register(TAG)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'id', 'slug',
    search_fields = 'id', 'slug', 'name',
    list_per_page = 20
    list_editable = 'name',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('name',),
    }
