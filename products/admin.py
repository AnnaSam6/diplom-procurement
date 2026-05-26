from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path
from .models import Category, Product, ProductCharacteristic
from .import_service import import_products_from_yaml


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'supplier', 'stock']
    change_list_template = "admin/products_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import/', self.admin_site.admin_view(self.import_view), name='products-import'),
        ]
        return custom_urls + urls

    def import_view(self, request):
        if request.method == 'POST':
            file_path = request.POST.get('file_path')
            supplier_id = request.POST.get('supplier_id')
            if file_path and supplier_id:
                try:
                    count = import_products_from_yaml(file_path, int(supplier_id))
                    self.message_user(request, f'Импортировано товаров: {count}', messages.SUCCESS)
                except Exception as e:
                    self.message_user(request, f'Ошибка: {e}', messages.ERROR)
            return redirect('admin:products_product_changelist')
        return redirect('admin:products_product_changelist')


@admin.register(ProductCharacteristic)
class ProductCharacteristicAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value']
