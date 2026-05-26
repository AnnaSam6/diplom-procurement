from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem, Address
from .serializers import OrderSerializer, CreateOrderSerializer
from .services import send_order_confirmation, send_order_notification_to_admin
from cart.models import CartItem


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)

        address, _ = Address.objects.get_or_create(
            user=request.user,
            city=serializer.validated_data['city'],
            street=serializer.validated_data['street'],
            house=serializer.validated_data['house']
        )

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total_price,
            status='pending'
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=cart_item.product.name,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        cart_items.delete()

        try:
            send_order_confirmation(order)
            send_order_notification_to_admin(order)
        except Exception as e:
            print(f'Ошибка отправки email: {e}')

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        order = self.get_object()

        allowed_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']

        new_status = request.data.get('status')

        if new_status not in allowed_statuses:
            return Response(
                {'error': f'Недопустимый статус. Доступны: {allowed_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        return Response(OrderSerializer(order).data)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('items')
        return Response(OrderSerializer(orders, many=True).data)

    @action(detail=False, methods=['get'])
    def supplier_orders(self, request):
        if not request.user.is_supplier:
            return Response({'error': 'Только для поставщиков'}, status=status.HTTP_403_FORBIDDEN)

        orders = Order.objects.filter(
            items__product_name__in=request.user.products.values_list('name', flat=True)
        ).distinct().prefetch_related('items')

        return Response(OrderSerializer(orders, many=True).data)

    @action(detail=False, methods=['post'])
    def toggle_accepting(self, request):
        if not request.user.is_supplier:
            return Response({'error': 'Только для поставщиков'}, status=status.HTTP_403_FORBIDDEN)

        request.user.is_active = not request.user.is_active
        request.user.save()

        status_text = 'принимает' if request.user.is_active else 'не принимает'
        return Response({'message': f'Поставщик теперь {status_text} заказы'})
