from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
  
    model = OrderItem
    extra = 0  # don't show extra empty rows by default
    readonly_fields = ("product", "quantity", "unit_price", "line_total")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ("id", "user", "status", "payment_method", "total_amount", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("id", "user__username", "shipping_address__city")
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = ("order", "product", "quantity", "unit_price", "line_total")
    search_fields = ("order__id", "product__name")