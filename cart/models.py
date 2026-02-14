from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class Cart(models.Model):
    """Cart Model for authenticated users"""
    user = models.ForeignKey(User, related_name='carts', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-added_at']
        unique_together = ['user', 'product']  # One cart entry per product per user
    
    def __str__(self):
        return f'{self.user.username} - {self.product.name} ({self.quantity})'
    
    def get_total_price(self):
        return self.product.price * self.quantity
    
    def update_quantity(self, quantity):
        if quantity > 0 and quantity <= self.product.stock:
            self.quantity = quantity
            self.save()
            return True
        return False
