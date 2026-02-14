from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.product_list, name='product_list'),
    path('shop/category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('shop/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('search/ajax/', views.search_ajax, name='search_ajax'),
]
