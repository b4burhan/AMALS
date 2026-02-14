from django.contrib import admin
from .models import Category, Product, Review, Newsletter, Testimonial


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'featured', 'created_at']
    list_filter = ['available', 'featured', 'created_at', 'category']
    list_editable = ['price', 'stock', 'available', 'featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    inlines = [ReviewInline]
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category')
        }),
        ('Product Info', {
            'fields': ('image', 'description', 'price', 'stock')
        }),
        ('Status', {
            'fields': ('available', 'featured')
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'review_text']
    readonly_fields = ['created_at']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected subscriptions as active"
    
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected subscriptions as inactive"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'rating', 'is_active', 'created_at']
    list_filter = ['is_active', 'rating', 'created_at']
    search_fields = ['name', 'position', 'content']
    list_editable = ['is_active']
