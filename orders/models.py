from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class Order(models.Model):
    """Order Model"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    
    # Order Information
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    
    # Shipping Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    
    # Order Details
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    
    # Status
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    
    # Notes
    notes = models.TextField(blank=True, help_text='Additional notes for the order')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Order #{self.order_number} - {self.full_name}'
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Generate unique order number"""
        import random
        import string
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f'ORD-{timestamp}-{random_str}'
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def get_subtotal(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total(self):
        return self.get_subtotal() + self.shipping_cost


class OrderItem(models.Model):
    """Order Item Model"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
    def get_total_price(self):
        return self.price * self.quantity
