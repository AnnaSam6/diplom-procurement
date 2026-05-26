from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Category, ProductCharacteristic
from .serializers import ProductSerializer, CategorySerializer, CharacteristicSerializer
from .import_service import import_products_from_yaml


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_available=True).prefetch_related('characteristics')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def import_products(self, request):
        if not request.user.is_supplier:
            return Response(
                {'error': 'Только поставщики могут импортировать товары'},
                status=status.HTTP_403_FORBIDDEN
            )

        file_path = request.data.get('file_path')
        if not file_path:
            return Response(
                {'error': 'Укажите путь к файлу (file_path)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            count = import_products_from_yaml(file_path, request.user.id)
            return Response({'message': f'Импортировано новых товаров: {count}'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_characteristic(self, request, pk=None):
        product = self.get_object()

        if not request.user.is_supplier:
            return Response(
                {'error': 'Только поставщики могут добавлять характеристики'},
                status=status.HTTP_403_FORBIDDEN
            )

        name = request.data.get('name')
        value = request.data.get('value')

        if not name or not value:
            return Response(
                {'error': 'Поля name и value обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )

        char, created = ProductCharacteristic.objects.update_or_create(
            product=product,
            name=name,
            defaults={'value': value}
        )

        return Response(
            CharacteristicSerializer(char).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
