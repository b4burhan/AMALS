#!/usr/bin/env python
"""
Dummy Data Generator for Django E-Commerce
Run this script to populate the database with sample data.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ecommerce.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from shop.models import Category, Product, Review, Testimonial, Newsletter
from blog.models import BlogPost, Comment
from cart.models import Cart
from orders.models import Order, OrderItem
from decimal import Decimal
import random


def create_superuser():
    """Create a superuser if it doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✓ Superuser created: admin / admin123")
    else:
        print("✓ Superuser already exists")


def create_categories():
    """Create sample categories"""
    categories_data = [
        {
            'name': 'Electronics',
            'description': 'Latest gadgets and electronic devices including smartphones, laptops, and accessories.'
        },
        {
            'name': 'Fashion',
            'description': 'Trendy clothing, shoes, and accessories for men and women.'
        },
        {
            'name': 'Home & Living',
            'description': 'Everything you need to make your home comfortable and stylish.'
        },
        {
            'name': 'Sports & Outdoors',
            'description': 'Sports equipment, outdoor gear, and fitness accessories.'
        },
        {
            'name': 'Books & Media',
            'description': 'Physical books, e-books, movies, and music.'
        }
    ]
    
    categories = []
    for data in categories_data:
        category, created = Category.objects.get_or_create(
            name=data['name'],
            defaults={'description': data['description']}
        )
        categories.append(category)
        if created:
            print(f"✓ Category created: {category.name}")
    
    return categories


def create_products(categories):
    """Create sample products"""
    products_data = [
        # Electronics
        {'name': 'Wireless Bluetooth Headphones', 'category': 0, 'price': 79.99, 'stock': 50, 'featured': True,
         'description': 'Premium wireless headphones with noise cancellation and 30-hour battery life.'},
        {'name': 'Smart Watch Pro', 'category': 0, 'price': 249.99, 'stock': 30, 'featured': True,
         'description': 'Advanced fitness tracking, heart rate monitor, and smartphone notifications.'},
        {'name': 'Portable Power Bank 20000mAh', 'category': 0, 'price': 39.99, 'stock': 100, 'featured': False,
         'description': 'High-capacity power bank with fast charging support for all devices.'},
        {'name': 'Wireless Charging Pad', 'category': 0, 'price': 29.99, 'stock': 75, 'featured': False,
         'description': 'Fast wireless charging for Qi-enabled smartphones.'},
        
        # Fashion
        {'name': 'Classic Cotton T-Shirt', 'category': 1, 'price': 24.99, 'stock': 200, 'featured': True,
         'description': 'Comfortable 100% cotton t-shirt available in multiple colors.'},
        {'name': 'Denim Jacket', 'category': 1, 'price': 89.99, 'stock': 40, 'featured': True,
         'description': 'Stylish denim jacket with classic design and modern fit.'},
        {'name': 'Running Shoes', 'category': 1, 'price': 119.99, 'stock': 60, 'featured': False,
         'description': 'Lightweight running shoes with cushioned sole for maximum comfort.'},
        {'name': 'Leather Wallet', 'category': 1, 'price': 49.99, 'stock': 80, 'featured': False,
         'description': 'Genuine leather wallet with multiple card slots and bill compartments.'},
        
        # Home & Living
        {'name': 'Smart LED Desk Lamp', 'category': 2, 'price': 59.99, 'stock': 45, 'featured': True,
         'description': 'Adjustable LED lamp with multiple brightness levels and color temperatures.'},
        {'name': 'Aromatherapy Diffuser', 'category': 2, 'price': 34.99, 'stock': 90, 'featured': False,
         'description': 'Ultrasonic essential oil diffuser with 7 color LED lights.'},
        {'name': 'Memory Foam Pillow', 'category': 2, 'price': 44.99, 'stock': 70, 'featured': False,
         'description': 'Ergonomic memory foam pillow for better sleep quality.'},
        {'name': 'Kitchen Knife Set', 'category': 2, 'price': 79.99, 'stock': 35, 'featured': True,
         'description': 'Professional 6-piece knife set with wooden block.'},
        
        # Sports & Outdoors
        {'name': 'Yoga Mat Premium', 'category': 3, 'price': 39.99, 'stock': 120, 'featured': True,
         'description': 'Non-slip yoga mat with carrying strap. 6mm thick for comfort.'},
        {'name': 'Resistance Bands Set', 'category': 3, 'price': 24.99, 'stock': 150, 'featured': False,
         'description': 'Set of 5 resistance bands with different strength levels.'},
        {'name': 'Stainless Steel Water Bottle', 'category': 3, 'price': 29.99, 'stock': 200, 'featured': False,
         'description': 'Insulated water bottle keeps drinks cold for 24 hours or hot for 12 hours.'},
        {'name': 'Camping Tent 4-Person', 'category': 3, 'price': 149.99, 'stock': 25, 'featured': True,
         'description': 'Waterproof camping tent with easy setup and ventilation windows.'},
        
        # Books & Media
        {'name': 'Python Programming Book', 'category': 4, 'price': 44.99, 'stock': 60, 'featured': True,
         'description': 'Comprehensive guide to Python programming for beginners and advanced users.'},
        {'name': 'Wireless Earbuds', 'category': 0, 'price': 59.99, 'stock': 85, 'featured': False,
         'description': 'True wireless earbuds with charging case and touch controls.'},
        {'name': 'Coffee Maker', 'category': 2, 'price': 99.99, 'stock': 40, 'featured': True,
         'description': 'Programmable coffee maker with thermal carafe.'},
        {'name': 'Fitness Tracker', 'category': 0, 'price': 69.99, 'stock': 55, 'featured': False,
         'description': 'Activity tracker with step counter, sleep monitor, and heart rate sensor.'},
    ]
    
    products = []
    for data in products_data:
        product, created = Product.objects.get_or_create(
            name=data['name'],
            defaults={
                'category': categories[data['category']],
                'price': Decimal(str(data['price'])),
                'stock': data['stock'],
                'featured': data['featured'],
                'description': data['description'],
                'available': True
            }
        )
        products.append(product)
        if created:
            print(f"✓ Product created: {product.name}")
    
    return products


def create_reviews(products, users):
    """Create sample reviews"""
    review_texts = [
        "Great product! Exactly what I was looking for.",
        "Good quality for the price. Would recommend.",
        "Excellent! Fast shipping and great customer service.",
        "Pretty good, but could be better.",
        "Amazing product! Exceeded my expectations.",
        "Decent quality, but not as described.",
        "Love it! Will definitely buy again.",
        "Good value for money. Happy with my purchase."
    ]
    
    for product in products:
        # Create 2-5 reviews per product
        num_reviews = random.randint(2, 5)
        for _ in range(num_reviews):
            user = random.choice(users)
            # Check if user already reviewed this product
            if not Review.objects.filter(product=product, user=user).exists():
                Review.objects.create(
                    product=product,
                    user=user,
                    rating=random.randint(3, 5),
                    review_text=random.choice(review_texts)
                )
    
    print(f"✓ Reviews created for products")


def create_blog_posts(categories, users):
    """Create sample blog posts"""
    blog_data = [
        {
            'title': '10 Tips for Smart Online Shopping',
            'category': 0,
            'author': 0,
            'featured': True,
            'content': '<p>Online shopping has revolutionized the way we buy products. Here are 10 tips to help you shop smarter...</p><h3>1. Compare Prices</h3><p>Always compare prices across different platforms before making a purchase.</p><h3>2. Read Reviews</h3><p>Customer reviews provide valuable insights into product quality.</p><h3>3. Check Return Policies</h3><p>Make sure you understand the return policy before buying.</p>'
        },
        {
            'title': 'The Future of E-Commerce in 2024',
            'category': 0,
            'author': 0,
            'featured': True,
            'content': '<p>The e-commerce landscape is constantly evolving. In 2024, we expect to see several key trends...</p><h3>AI-Powered Shopping</h3><p>Artificial intelligence is transforming the shopping experience with personalized recommendations.</p><h3>Sustainable Shopping</h3><p>Consumers are increasingly conscious of environmental impact.</p>'
        },
        {
            'title': 'How to Choose the Perfect Headphones',
            'category': 0,
            'author': 1,
            'featured': False,
            'content': '<p>With so many options available, choosing the right headphones can be overwhelming...</p><h3>Types of Headphones</h3><p>Over-ear, on-ear, and in-ear headphones each have their advantages.</p><h3>Sound Quality</h3><p>Look for headphones with good frequency response and low distortion.</p>'
        },
        {
            'title': 'Home Office Setup Guide',
            'category': 2,
            'author': 1,
            'featured': True,
            'content': '<p>Creating an efficient home office is essential for productivity...</p><h3>Ergonomic Furniture</h3><p>Invest in a good chair and desk to prevent back pain.</p><h3>Lighting</h3><p>Proper lighting reduces eye strain and improves focus.</p>'
        },
        {
            'title': 'Fitness Tips for Beginners',
            'category': 3,
            'author': 2,
            'featured': False,
            'content': '<p>Starting a fitness journey can be intimidating, but it doesn\'t have to be...</p><h3>Start Slow</h3><p>Begin with manageable workouts and gradually increase intensity.</p><h3>Consistency is Key</h3><p>Regular exercise is more important than intense workouts.</p>'
        },
        {
            'title': 'Summer Fashion Trends 2024',
            'category': 1,
            'author': 2,
            'featured': False,
            'content': '<p>Discover the hottest fashion trends for this summer...</p><h3>Bright Colors</h3><p>This summer is all about bold, vibrant colors.</p><h3>Sustainable Fashion</h3><p>Eco-friendly materials are becoming increasingly popular.</p>'
        },
        {
            'title': 'Best Books for Personal Development',
            'category': 4,
            'author': 0,
            'featured': False,
            'content': '<p>Reading is one of the best ways to invest in yourself...</p><h3>Atomic Habits</h3><p>James Clear\'s guide to building good habits and breaking bad ones.</p><h3>The 7 Habits of Highly Effective People</h3><p>Stephen Covey\'s classic on personal effectiveness.</p>'
        },
        {
            'title': 'Camping Essentials Checklist',
            'category': 3,
            'author': 1,
            'featured': False,
            'content': '<p>Before you head out on your next camping trip, make sure you have these essentials...</p><h3>Shelter</h3><p>A reliable tent and sleeping bag are crucial.</p><h3>Cooking Gear</h3><p>Portable stove, cookware, and utensils.</p>'
        }
    ]
    
    for data in blog_data:
        post, created = BlogPost.objects.get_or_create(
            title=data['title'],
            defaults={
                'category': categories[data['category']],
                'author': users[data['author']],
                'content': data['content'],
                'status': 'approved',
                'is_featured': data['featured'],
                'views': random.randint(100, 1000)
            }
        )
        if created:
            print(f"✓ Blog post created: {post.title}")


def create_testimonials():
    """Create sample testimonials"""
    testimonials_data = [
        {
            'name': 'Sarah Johnson',
            'position': 'Regular Customer',
            'content': 'Amazing shopping experience! Fast delivery and excellent customer service. Will definitely shop here again.',
            'rating': 5
        },
        {
            'name': 'Michael Chen',
            'position': 'Verified Buyer',
            'content': 'Great product quality at reasonable prices. The blog articles are also very helpful!',
            'rating': 5
        },
        {
            'name': 'Emily Davis',
            'position': 'Fashion Enthusiast',
            'content': 'Love the variety of products. The checkout process is smooth and hassle-free.',
            'rating': 4
        },
        {
            'name': 'David Wilson',
            'position': 'Tech Lover',
            'content': 'Best electronics store online. Products are genuine and well-packaged.',
            'rating': 5
        },
        {
            'name': 'Lisa Anderson',
            'position': 'Home Decorator',
            'content': 'Found exactly what I needed for my home. The product descriptions are accurate.',
            'rating': 4
        },
        {
            'name': 'James Brown',
            'position': 'Fitness Trainer',
            'content': 'Excellent sports equipment selection. Fast shipping and great prices!',
            'rating': 5
        }
    ]
    
    for data in testimonials_data:
        testimonial, created = Testimonial.objects.get_or_create(
            name=data['name'],
            defaults={
                'position': data['position'],
                'content': data['content'],
                'rating': data['rating'],
                'is_active': True
            }
        )
        if created:
            print(f"✓ Testimonial created: {testimonial.name}")


def create_regular_users():
    """Create regular user accounts"""
    users_data = [
        {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
    ]
    
    users = []
    for data in users_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name']
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print(f"✓ User created: {user.username} / testpass123")
        users.append(user)
    
    # Add admin to users list
    admin = User.objects.get(username='admin')
    users.append(admin)
    
    return users


def main():
    """Main function to generate all dummy data"""
    print("=" * 50)
    print("Django E-Commerce Dummy Data Generator")
    print("=" * 50)
    print()
    
    # Create superuser
    create_superuser()
    print()
    
    # Create regular users
    users = create_regular_users()
    print()
    
    # Create categories
    categories = create_categories()
    print()
    
    # Create products
    products = create_products(categories)
    print()
    
    # Create reviews
    create_reviews(products, users)
    print()
    
    # Create blog posts
    create_blog_posts(categories, users)
    print()
    
    # Create testimonials
    create_testimonials()
    print()
    
    print("=" * 50)
    print("Dummy data generation complete!")
    print("=" * 50)
    print()
    print("Login credentials:")
    print("  Admin: admin / admin123")
    print("  Users: john_doe, jane_smith, mike_wilson / testpass123")


if __name__ == '__main__':
    main()
