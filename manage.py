# models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# serializers.py

from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price']

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer

class ProductByCategoryView(APIView):
    """
    API View to get products filtered by category ID.
    Endpoint: /api/products/by-category/?category_id=<id>
    """

    def get(self, request):
        category_id = request.query_params.get('category_id')

        # Check if category_id is provided
        if not category_id:
            return Response({'error': 'category_id query parameter is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate category exists
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        # Filter and return products in that category
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# urls.py

from django.urls import path
from .views import ProductByCategoryView

urlpatterns = [
    path('api/products/by-category/', ProductByCategoryView.as_view(), name='products-by-category'),
]
