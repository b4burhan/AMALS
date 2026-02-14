from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'added_at', 'get_total_price']
    list_filter = ['added_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['added_at']
