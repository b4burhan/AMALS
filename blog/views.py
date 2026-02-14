from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import BlogPost, Comment, BlogSubmission
from shop.models import Category
from .forms import CommentForm, BlogSubmissionForm


def blog_list(request, category_slug=None):
    """Blog list view with category filter"""
    category = None
    categories = Category.objects.all()
    posts = BlogPost.objects.filter(status='approved')
    
    # Category filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    # Featured posts
    featured_posts = posts.filter(is_featured=True)[:3]
    
    # Pagination
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'categories': categories,
        'posts': posts,
        'featured_posts': featured_posts,
        'query': query,
    }
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    """Blog detail view"""
    post = get_object_or_404(BlogPost, slug=slug, status='approved')
    
    # Increment views
    post.increment_views()
    
    # Get approved comments
    comments = post.comments.filter(approved=True)
    
    # Related posts (same category, exclude current)
    related_posts = BlogPost.objects.filter(
        category=post.category,
        status='approved'
    ).exclude(id=post.id)[:4]
    
    # Comment form
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
            return redirect('blog:post_detail', slug=slug)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
        'form': form,
    }
    return render(request, 'blog/blog_detail.html', context)


@login_required
def submit_blog(request):
    """Submit blog post for approval"""
    if request.method == 'POST':
        form = BlogSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            messages.success(
                request, 
                'Your blog post has been submitted for review. You will be notified once it is approved.'
            )
            return redirect('blog:post_list')
    else:
        form = BlogSubmissionForm()
    
    context = {
        'form': form,
    }
    return render(request, 'blog/submit_blog.html', context)


@login_required
def my_submissions(request):
    """View user's blog submissions"""
    submissions = BlogSubmission.objects.filter(user=request.user).order_by('-submitted_at')
    
    context = {
        'submissions': submissions,
    }
    return render(request, 'blog/my_submissions.html', context)
