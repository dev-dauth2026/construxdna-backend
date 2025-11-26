from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from .services import create_order_for_user


class OrderViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - GET /api/orders/          -> list orders of current user
    - GET /api/orders/{id}/     -> retrieve a single order
    - POST /api/orders/         -> create new order

    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Only allow users to see THEIR orders
        return Order.objects.filter(user=self.request.user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        """
        Override create to use OrderCreateSerializer and services.create_order_for_user.
        """
        input_serializer = OrderCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            order = create_order_for_user(
                user=request.user,
                shipping_address_id=input_serializer.validated_data["shipping_address_id"],
                payment_method=input_serializer.validated_data["payment_method"],
                items_data=input_serializer.validated_data["items"],
            )
        except ValueError as e:
            # Business logic error (e.g. not enough stock, invalid address)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)