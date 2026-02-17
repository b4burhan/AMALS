from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='post_list'),
    path('category/<slug:category_slug>/', views.blog_list, name='post_list_by_category'),
    path('submit/new/', views.submit_blog, name='submit_blog'),       # move above slug
    path('my-submissions/', views.my_submissions, name='my_submissions'),  # move above slug
    path('<slug:slug>/', views.blog_detail, name='post_detail'),       # keep generic slug LAST
]

