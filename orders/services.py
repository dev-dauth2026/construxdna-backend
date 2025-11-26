from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from catalog.models import Product
from accounts.models import Address
from .models import Order, OrderItem


@transaction.atomic
def create_order_for_user(user, shipping_address_id, payment_method, items_data):
   
    try:
        address = Address.objects.get(id=shipping_address_id, user=user)
    except ObjectDoesNotExist:
        raise ValueError("Invalid shipping address")

    # Create the order first (without total_amount)
    order = Order.objects.create(
        user=user,
        shipping_address=address,
        payment_method=payment_method,
    )

    total = Decimal("0.00")

    for item in items_data:
        product_id = item["product_id"]
        quantity = item["quantity"]

        # Lock product row to avoid stock race conditions
        product = Product.objects.select_for_update().get(id=product_id, is_active=True)

        if product.stock_quantity < quantity:
            raise ValueError(f"Not enough stock for product: {product.name}")

        unit_price = product.price
        line_total = unit_price * quantity

        # Create order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            line_total=line_total,
        )

        # Decrease stock
        product.stock_quantity -= quantity
        product.save()

        total += line_total

    # Update order total
    order.total_amount = total
    order.save()

    return order