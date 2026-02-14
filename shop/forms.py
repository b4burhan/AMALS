from django import forms
from .models import Review, Newsletter


class ReviewForm(forms.ModelForm):
    """Form for submitting product reviews"""
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'rating-input'}),
        label='Rating'
    )
    
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review here...'
            }),
        }


class NewsletterForm(forms.ModelForm):
    """Form for newsletter subscription"""
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Newsletter.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already subscribed.')
        return email


class ContactForm(forms.Form):
    """Contact form"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Your Message'
        })
    )
