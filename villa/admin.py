from django.contrib import admin

from .models import Apartment, ApartmentCategory, Basket


@admin.register(ApartmentCategory)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'description']


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'country', 'city', 'category', 'price']
    list_select_related = ['category']
    list_filter = ['city', 'country', 'category']
    # list_editable = ['country']
    search_help_text = 'Поиск по полю name'
    date_hierarchy = 'when_was_built'


class BasketAdmin(admin.TabularInline):
    model = Basket
    extra = 0
