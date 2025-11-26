from rest_framework.viewsets import ModelViewSet
from product.models import Category
from product.serializers.category_serializer import CategorySerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer