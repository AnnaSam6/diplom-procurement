import yaml
from .models import Product, Category, ProductCharacteristic
from django.contrib.auth import get_user_model

User = get_user_model()


def import_products_from_yaml(file_path, supplier_id):
    """Импорт товаров из YAML-файла с характеристиками"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    supplier = User.objects.get(id=supplier_id)
    created_count = 0

    for item in data.get('products', []):
        category, _ = Category.objects.get_or_create(name=item['category'])

        product, created = Product.objects.update_or_create(
            name=item['name'],
            supplier=supplier,
            defaults={
                'description': item.get('description', ''),
                'price': item['price'],
                'category': category,
                'stock': item.get('stock', 0),
                'is_available': item.get('is_available', True),
            }
        )

        if 'characteristics' in item:
            for name, value in item['characteristics'].items():
                ProductCharacteristic.objects.update_or_create(
                    product=product,
                    name=name,
                    defaults={'value': value}
                )

        if created:
            created_count += 1

    return created_count
