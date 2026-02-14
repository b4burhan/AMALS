from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from cart.models import Cart
from shop.models import Product
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout(request):
    """Checkout view"""
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
    
    # Calculate totals
    subtotal = sum(
        (item.get_total_price() for item in cart_items),
        Decimal('0.00')
    )

    free_shipping_threshold = Decimal('100.00')
    shipping_cost = Decimal('10.00') if subtotal < free_shipping_threshold else Decimal('0.00')

    total = subtotal + shipping_cost

    
    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create order
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_amount = total
                    order.shipping_cost = shipping_cost
                    order.save()
                    
                    # Create order items and update stock
                    for cart_item in cart_items:
                        # Check stock availability
                        if cart_item.quantity > cart_item.product.stock:
                            raise ValueError(f'Not enough stock for {cart_item.product.name}')
                        
                        OrderItem.objects.create(
                            order=order,
                            product=cart_item.product,
                            price=cart_item.product.price,
                            quantity=cart_item.quantity
                        )
                        
                        # Update product stock
                        cart_item.product.stock -= cart_item.quantity
                        cart_item.product.save()
                    
                    # Clear cart
                    cart_items.delete()
                    
                    messages.success(request, f'Order placed successfully! Your order number is {order.order_number}')
                    return redirect('orders:order_confirmation', order_id=order.id)
                    
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'An error occurred while processing your order. Please try again. Error: {e}')
    else:
        form = CheckoutForm(user=request.user)
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_confirmation.html', context)


@login_required
def order_history(request):
    """User order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_history.html', context)


@login_required
def order_detail(request, order_id):
    """Order detail view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)
