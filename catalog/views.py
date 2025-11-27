from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
   
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
   
    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "name", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()

        category_slug = self.request.query_params.get("category")
        brand_id = self.request.query_params.get("brand")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        new_only = self.request.query_params.get("new")

        # Filter by Category (slug)
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        # Filter by Brand (id or name)
        if brand_id:
            qs = qs.filter(brand_id=brand_id)

        # Price range filter
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)

        # "new products" (last 7 days)
        if new_only == "true":
            from datetime import timedelta
            from django.utils import timezone

            last_week = timezone.now() - timedelta(days=7)
            qs = qs.filter(created_at__gte=last_week)

        return qs
