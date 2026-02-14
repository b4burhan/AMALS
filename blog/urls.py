from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='post_list'),
    path('category/<slug:category_slug>/', views.blog_list, name='post_list_by_category'),
    path('<slug:slug>/', views.blog_detail, name='post_detail'),
    path('submit/new/', views.submit_blog, name='submit_blog'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
]
