from rest_framework import serializers
from .models import Order, OrderItem
from accounts.models import Address


class OrderItemCreateSerializer(serializers.Serializer):
    """
    Used when creating an order (input).
    Only needs product_id and quantity.
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Used when returning order details (output).
    Includes product name.
    """
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "quantity", "unit_price", "line_total"]


class OrderSerializer(serializers.ModelSerializer):
    """
    Used for listing and retrieving orders.
    Read-only items and amount fields.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(),
        source="shipping_address",
        write_only=True,
        required=False,  # we won't use this for listing
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "payment_method",
            "total_amount",
            "created_at",
            "shipping_address_id",
            "items",
        ]
        read_only_fields = ["status", "total_amount", "created_at", "items"]


class OrderCreateSerializer(serializers.Serializer):
    """
    Used only for order creation (input).
    """
    shipping_address_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=["COD", "BANK_TRANSFER"])
    items = OrderItemCreateSerializer(many=True)

    def validate(self, attrs):
        if not attrs.get("items"):
            raise serializers.ValidationError("Order must contain at least one item.")
        return attrs