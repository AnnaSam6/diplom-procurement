from rest_framework import serializers
from .models import Order, OrderItem, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'city', 'street', 'house']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address_info = serializers.StringRelatedField(source='address', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'address', 'address_info', 'status', 'status_display',
                  'total_price', 'created_at', 'items']


class CreateOrderSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=200)
    house = serializers.CharField(max_length=20)