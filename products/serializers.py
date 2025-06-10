
from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True) # Read-only for nested representation
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, allow_null=True
    ) # For writing/updating product with category ID

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock',
            'category', 'category_id', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['created_at', 'updated_at']