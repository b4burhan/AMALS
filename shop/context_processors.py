from .models import Category


def shop_context(request):
    """Context processor to add categories to all templates"""
    categories = Category.objects.all()[:6]
    return {
        'header_categories': categories,
    }
