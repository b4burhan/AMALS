from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Category, Product, Review, Newsletter, Testimonial
from .forms import ReviewForm, NewsletterForm, ContactForm


def home(request):
    """Home page view"""
    featured_products = Product.objects.filter(featured=True, available=True)[:8]
    latest_products = Product.objects.filter(available=True)[:8]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'testimonials': testimonials,
    }
    return render(request, 'shop/home.html', context)


def product_list(request, category_slug=None):
    """Product list view with category filter"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Category filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
        'sort_by': sort_by,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, id, slug):
    """Product detail view"""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    # Get reviews
    reviews = product.reviews.all()
    
    # Check if user has already reviewed
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(product=product, user=request.user).exists()
    
    # Related products (same category, exclude current)
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    
    # Review form
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('shop:product_detail', id=id, slug=slug)
    else:
        form = ReviewForm()
    
    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'form': form,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'shop/product_detail.html', context)


def newsletter_subscribe(request):
    """Newsletter subscription view"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            messages.error(request, 'This email is already subscribed or invalid.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            subject = f"Contact Form: {form.cleaned_data['subject']}"
            message = f"From: {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n{form.cleaned_data['message']}"
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('contact')
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again.')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})


def search_ajax(request):
    """AJAX search for products"""
    query = request.GET.get('q', '')
    products = []
    
    if query:
        products_list = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            available=True
        )[:5]
        
        products = [{
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'price': str(p.price),
            'image': p.image.url if p.image else None,
        } for p in products_list]
    
    return JsonResponse({'products': products})


def custom_404(request, exception):
    """Custom 404 error page"""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error page"""
    return render(request, 'errors/500.html', status=500)
