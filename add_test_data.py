import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from products.models import Category, Product

# Создаём поставщика
supplier, created = User.objects.get_or_create(
    username='supplier1',
    defaults={
        'email': 'supplier1@example.com',
        'user_type': 'supplier'
    }
)
if created:
    supplier.set_password('supplier123')
    supplier.save()
    print('✅ Поставщик создан')
else:
    print('Поставщик уже существует')

# Создаём категории
categories = ['Электроника', 'Одежда', 'Продукты', 'Книги']
for cat_name in categories:
    cat, created = Category.objects.get_or_create(name=cat_name)
    if created:
        print(f'✅ Категория "{cat_name}" создана')

# Создаём товары
products_data = [
    ('Смартфон NZT', 'Отличный смартфон', 29990, 'Электроника', 50),
    ('Ноутбук AppPro', 'Мощный ноутбук', 89990, 'Электроника', 20),
    ('Джинсы скини', 'Синие джинсы', 3990, 'Одежда', 100),
    ('Футболка белая', 'Футболка черная', 990, 'Одежда', 200),
    ('Шоколад молочный', 'Вкусный шоколад', 150, 'Продукты', 500),
    ('Кофе молотый', 'Какао', 450, 'Продукты', 300),
    ('Python для начинающих', 'Философия', 1200, 'Книги', 30),
]

for name, desc, price, cat_name, stock in products_data:
    category = Category.objects.get(name=cat_name)
    product, created = Product.objects.get_or_create(
        name=name,
        defaults={
            'description': desc,
            'price': price,
            'category': category,
            'supplier': supplier,
            'stock': stock,
            'is_available': True
        }
    )
    if created:
        print(f'✅ Товар "{name}" создан')

print('\nГотово! Данные добавлены.')
print('Логин поставщика: supplier1')
print('Пароль поставщика: supplier123')