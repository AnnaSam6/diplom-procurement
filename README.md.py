# API для автоматизации закупок

Дипломный проект Python-разработчик

## Возможности

- Регистрация и авторизация пользователей
- Просмотр каталога товаров
- Добавление товаров в корзину
- Оформление заказов
- Импорт товаров из YAML
- Отправка email-уведомлений
- Документация API (Swagger)

## Установка и запуск

1. Установить виртуальное окружение:
python -m venv venv
venv\Scripts\activate

2. Установить зависимости:
pip install -r requirements.txt

3. Применить миграции:
python manage.py migrate

4. Загрузить тестовые данные:
python add_test_data.py

5. Запустить сервер:
python manage.py runserver

## Документация API

Swagger: http://127.0.0.1:8000/swagger/
ReDoc: http://127.0.0.1:8000/redoc/

## Тестовые пользователи

Админ: admin / admin123
Покупатель: buyer1 / buyer1234
Поставщик: supplier1 / supplier123