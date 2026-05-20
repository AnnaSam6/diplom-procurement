from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from .serializers import CartItemSerializer, AddToCartSerializer
from products.models import Product


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """Добавить товар в корзину"""
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        try:
            product = Product.objects.get(id=product_id, is_available=True)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def remove(self, request):
        """Удалить товар из корзины"""
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'product_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        CartItem.objects.filter(user=request.user, product_id=product_id).delete()
        return Response({'message': 'Товар удалён из корзины'})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Сводка по корзине"""
        items = self.get_queryset()
        total = sum(item.total_price for item in items)
        count = sum(item.quantity for item in items)

        return Response({
            'items': CartItemSerializer(items, many=True).data,
            'total_items': count,
            'total_price': str(total)
        })