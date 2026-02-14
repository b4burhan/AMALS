# Django E-Commerce + Blog Platform

A complete, production-ready Django e-commerce and blogging platform with modern UI, secure authentication, and comprehensive features.

## Features

### E-Commerce
- **Product Catalog**: Browse products with category filtering and search
- **Shopping Cart**: Add, update, and remove items with persistent cart
- **Checkout System**: Complete order processing with shipping information
- **Product Reviews**: Customers can rate and review products
- **Related Products**: Smart product recommendations

### Blog System
- **Blog Posts**: Rich text content with CKEditor
- **Categories**: Organized content by topics
- **Comments**: User engagement with comment system
- **Blog Submission**: Users can submit articles for admin approval
- **Featured Posts**: Highlight important articles

### User Management
- **Authentication**: Registration, login, logout, password reset
- **User Profiles**: Complete profile management with avatar upload
- **Order History**: Track past orders
- **Blog Submissions**: View submitted articles and their status

### Additional Features
- **Newsletter Subscription**: Email subscription system
- **Contact Form**: Send inquiries to admin
- **Responsive Design**: Mobile-first Bootstrap 5 design
- **SEO Optimized**: Meta tags and structured data
- **Toast Notifications**: User-friendly feedback messages

## Tech Stack

- **Backend**: Django 5.0+
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite (default), PostgreSQL (production-ready)
- **Rich Text**: CKEditor
- **Forms**: Django Crispy Forms

## Installation

### Prerequisites
- Python 3.10+
- pip
- virtualenv (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django_ecommerce
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Generate dummy data (optional)**
   ```bash
   python generate_dummy_data.py
   ```

6. **Create superuser (if not using dummy data)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Default Login Credentials

After running `generate_dummy_data.py`:

- **Admin**: username: `admin`, password: `admin123`
- **Users**: username: `john_doe`, `jane_smith`, `mike_wilson`, password: `testpass123`

## Project Structure

```
django_ecommerce/
├── django_ecommerce/       # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── shop/                   # Shop app (products, categories, reviews)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── blog/                   # Blog app (posts, comments, submissions)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── cart/                   # Cart app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── orders/                 # Orders app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── accounts/               # User accounts app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── templates/              # HTML templates
│   ├── base.html
│   ├── shop/
│   ├── blog/
│   ├── cart/
│   ├── orders/
│   ├── accounts/
│   └── errors/
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                  # User-uploaded files
├── manage.py
├── requirements.txt
├── generate_dummy_data.py
└── README.md
```

## Configuration

### Email Settings
Update email settings in `django_ecommerce/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Database Settings
For production, update the database settings in `django_ecommerce/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Security Settings
For production, update these settings:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'your-secure-secret-key'  # Change this!
```

## Admin Panel

The Django admin panel is customized for easy management:

- **Products**: Manage products with inline reviews
- **Categories**: Organize products and blog posts
- **Blog Posts**: Manage articles with inline comments
- **Blog Submissions**: Approve or reject user submissions
- **Orders**: Track and update order status
- **Users**: Manage user accounts and profiles

## API Endpoints

### Shop
- `GET /` - Home page
- `GET /shop/` - Product list
- `GET /shop/category/<slug>/` - Products by category
- `GET /shop/<id>/<slug>/` - Product detail
- `POST /newsletter/subscribe/` - Subscribe to newsletter
- `GET /search/ajax/?q=<query>` - AJAX product search

### Blog
- `GET /blog/` - Blog list
- `GET /blog/category/<slug>/` - Posts by category
- `GET /blog/<slug>/` - Blog post detail
- `GET /blog/submit/new/` - Submit blog post (login required)
- `GET /blog/my-submissions/` - View my submissions (login required)

### Cart
- `GET /cart/` - Cart detail
- `POST /cart/add/<product_id>/` - Add to cart
- `POST /cart/update/<cart_id>/` - Update quantity
- `GET /cart/remove/<cart_id>/` - Remove item
- `GET /cart/clear/` - Clear cart

### Orders
- `GET /orders/checkout/` - Checkout (login required)
- `GET /orders/confirmation/<order_id>/` - Order confirmation
- `GET /orders/history/` - Order history (login required)
- `GET /orders/detail/<order_id>/` - Order detail (login required)

### Accounts
- `GET /accounts/login/` - Login
- `GET /accounts/register/` - Register
- `GET /accounts/logout/` - Logout
- `GET /accounts/profile/` - Profile (login required)
- `GET /accounts/password-reset/` - Password reset

## Customization

### Styling
- Edit `static/css/style.css` for custom styles
- Bootstrap 5 variables can be customized

### Templates
- All templates use Bootstrap 5 classes
- Base template: `templates/base.html`
- Override templates in respective app folders

### Static Files
- CSS: `static/css/`
- JavaScript: `static/js/`
- Images: `static/images/`

## Deployment

### Using Gunicorn and Nginx

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create gunicorn config**
   ```bash
   gunicorn --bind 0.0.0.0:8000 django_ecommerce.wsgi:application
   ```

3. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location /static/ {
           alias /path/to/static/;
       }
       
       location /media/ {
           alias /path/to/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
       }
   }
   ```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD gunicorn django_ecommerce.wsgi:application --bind 0.0.0.0:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, email support@djangoshop.com or open an issue on GitHub.

## Acknowledgments

- Django Framework
- Bootstrap 5
- CKEditor
- Django Crispy Forms
