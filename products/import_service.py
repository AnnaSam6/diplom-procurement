import yaml
from .models import Product, Category


def import_products_from_yaml(file_path, supplier):
    """Импорт товаров из YAML файла"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    created_count = 0

    for item in data.get('products', []):
        category, _ = Category.objects.get_or_create(name=item['category'])

        product, created = Product.objects.get_or_create(
            name=item['name'],
            defaults={
                'description': item.get('description', ''),
                'price': item['price'],
                'category': category,
                'supplier': supplier,
                'stock': item.get('stock', 0),
            }
        )

        if created:
            created_count += 1

    return created_count