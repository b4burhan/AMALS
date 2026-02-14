from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from shop.models import Product
from .models import Cart
from .forms import CartAddProductForm, CartUpdateForm


@login_required
def cart_detail(request):
    """Cart detail view"""
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate totals
    total = sum(item.get_total_price() for item in cart_items)
    item_count = sum(item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'item_count': item_count,
    }
    return render(request, 'cart/cart_detail.html', context)


@login_required
@require_POST
def cart_add(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, available=True)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        
        # Check if product is already in cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if product already in cart
            new_quantity = cart_item.quantity + quantity
            if new_quantity <= product.stock:
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, f'Updated {product.name} quantity in your cart.')
            else:
                messages.warning(request, f'Cannot add more {product.name}. Maximum stock reached.')
        else:
            messages.success(request, f'Added {product.name} to your cart.')
    
    return redirect('cart:cart_detail')


@login_required
def cart_update(request, cart_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    if request.method == 'POST':
        form = CartUpdateForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            if quantity <= cart_item.product.stock:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cart updated successfully.')
            else:
                messages.warning(request, f'Only {cart_item.product.stock} items available in stock.')
    
    return redirect('cart:cart_detail')


@login_required
def cart_remove(request, cart_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Removed {product_name} from your cart.')
    return redirect('cart:cart_detail')


@login_required
def cart_clear(request):
    """Clear all items from cart"""
    Cart.objects.filter(user=request.user).delete()
    messages.success(request, 'Your cart has been cleared.')
    return redirect('cart:cart_detail')


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
