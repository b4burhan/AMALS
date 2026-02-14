from django import forms
from .models import Comment, BlogSubmission
from shop.models import Category


class CommentForm(forms.ModelForm):
    """Form for submitting blog comments"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            }),
        }


class BlogSubmissionForm(forms.ModelForm):
    """Form for submitting blog posts (requires admin approval)"""
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = BlogSubmission
        fields = ['title', 'category', 'featured_image', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog title'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your blog content here...'
            }),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise forms.ValidationError('Title must be at least 10 characters long.')
        return title
