from django.contrib import admin
from django.utils import timezone
from .models import BlogPost, Comment, BlogSubmission


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['created_at']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'is_featured', 'created_at']
    list_filter = ['status', 'is_featured', 'created_at', 'category']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    date_hierarchy = 'created_at'
    inlines = [CommentInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('featured_image', 'content', 'excerpt')
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'views')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'user', 'approved', 'created_at']
    list_filter = ['approved', 'created_at']
    search_fields = ['blog__title', 'user__username', 'content']
    list_editable = ['approved']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(approved=False)
    disapprove_comments.short_description = "Disapprove selected comments"


@admin.register(BlogSubmission)
class BlogSubmissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'status', 'submitted_at', 'reviewed_at']
    list_filter = ['status', 'submitted_at', 'category']
    search_fields = ['title', 'user__username', 'content']
    readonly_fields = ['submitted_at', 'reviewed_at', 'reviewed_by']
    actions = ['approve_submissions', 'reject_submissions']
    
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'category')
        }),
        ('Content', {
            'fields': ('featured_image', 'content')
        }),
        ('Review', {
            'fields': ('status', 'admin_notes', 'submitted_at', 'reviewed_at', 'reviewed_by')
        }),
    )
    
    def approve_submissions(self, request, queryset):
        for submission in queryset.filter(status='pending'):
            submission.approve(request.user)
        self.message_user(request, f'{queryset.filter(status="pending").count()} submissions approved.')
    approve_submissions.short_description = "Approve selected submissions"

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = BlogSubmission.objects.get(pk=obj.pk)

            # If status changed to approved
            if old_obj.status != 'approved' and obj.status == 'approved':
                super().save_model(request, obj, form, change)
                obj.approve(request.user)
                return

        super().save_model(request, obj, form, change)

    
    def reject_submissions(self, request, queryset):
        for submission in queryset.filter(status='pending'):
            submission.reject(request.user, 'Rejected by admin')
        self.message_user(request, f'{queryset.filter(status="pending").count()} submissions rejected.')
    reject_submissions.short_description = "Reject selected submissions"
