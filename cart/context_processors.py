from .models import Cart


def cart_context(request):
    """Context processor for cart info in all templates"""
    cart_items = []
    cart_total = 0
    cart_item_count = 0
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_total = sum(item.get_total_price() for item in cart_items)
        cart_item_count = sum(item.quantity for item in cart_items)
    
    return {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_item_count': cart_item_count,
    }
