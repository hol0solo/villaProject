from django.contrib import admin

from orders.models import PreOrder


@admin.register(PreOrder)
class PreOrderAdmin(admin.ModelAdmin):
    list_display = ['initiator', 'name', 'surname', 'agent', 'status']
    readonly_fields = ['id', 'creation_date']
