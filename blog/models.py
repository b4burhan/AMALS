from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from shop.models import Category


class BlogPost(models.Model):
    """Blog Post Model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='blog_posts', on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True, null=True)
    content = RichTextField()
    excerpt = models.TextField(blank=True, help_text='Brief summary of the post')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt and self.content:
            # Create excerpt from content (first 200 characters)
            plain_text = self.content[:200]
            self.excerpt = plain_text[:200] + '...' if len(plain_text) > 200 else plain_text
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    
    def get_comments_count(self):
        return self.comments.filter(approved=True).count()
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Comment(models.Model):
    """Blog Comment Model"""
    blog = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='blog_comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'


class BlogSubmission(models.Model):
    """Model for blog submission requests (before approval)"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, related_name='blog_submissions', on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='blog/submissions/%Y/%m/%d/', blank=True, null=True)
    content = RichTextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text='Notes from admin review')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_submissions')
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f'{self.title} by {self.user.username} ({self.status})'
    
    def approve(self, admin_user):
        """Approve the submission and create a blog post"""
        from django.utils import timezone
        
        blog_post = BlogPost.objects.create(
            title=self.title,
            author=self.user,
            category=self.category,
            featured_image=self.featured_image,
            content=self.content,
            status='approved'
        )
        
        self.status = 'approved'
        self.reviewed_at = timezone.now()
        self.reviewed_by = admin_user
        self.save()
        
        return blog_post
    
    def reject(self, admin_user, notes=''):
        """Reject the submission"""
        from django.utils import timezone
        
        self.status = 'rejected'
        self.reviewed_at = timezone.now()
        self.reviewed_by = admin_user
        self.admin_notes = notes
        self.save()
