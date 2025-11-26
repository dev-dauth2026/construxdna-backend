from rest_framework import serializers
from .models import Category, Brand, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ["id", "name", "website"]


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "unit",
            "price",
            "stock_quantity",
            "is_active",
            "image",
            "created_at",
            "category",
            "brand",
        ]