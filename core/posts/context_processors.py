from .models import Category

def categorys(requests):
    return {'categories': Category.objects.all()}