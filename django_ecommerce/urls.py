"""
URL configuration for django_ecommerce project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('blog/', include('blog.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'shop.views.custom_404'
handler500 = 'shop.views.custom_500'
