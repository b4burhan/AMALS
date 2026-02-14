from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total_price']
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'full_name', 'total_amount', 
        'payment_status', 'order_status', 'created_at'
    ]
    list_filter = ['payment_status', 'order_status', 'created_at']
    search_fields = ['order_number', 'full_name', 'email', 'user__username']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_editable = ['payment_status', 'order_status']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'total_amount', 'shipping_cost')
        }),
        ('Shipping Information', {
            'fields': ('full_name', 'email', 'phone', 'address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Status', {
            'fields': ('payment_status', 'order_status')
        }),
        ('Additional', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_processing(self, request, queryset):
        queryset.update(order_status='processing')
    mark_as_processing.short_description = "Mark selected orders as processing"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(order_status='shipped')
    mark_as_shipped.short_description = "Mark selected orders as shipped"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(order_status='delivered')
    mark_as_delivered.short_description = "Mark selected orders as delivered"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(order_status='cancelled')
    mark_as_cancelled.short_description = "Mark selected orders as cancelled"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity', 'get_total_price']
    list_filter = ['order__created_at']
    search_fields = ['order__order_number', 'product__name']
