from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation(order):
    """Отправка подтверждения заказа покупателю"""
    subject = f'Заказ №{order.id} оформлен'
    message = f'''
    Здравствуйте, {order.user.username}!

    Ваш заказ №{order.id} успешно оформлен.

    Состав заказа:
    '''

    for item in order.items.all():
        message += f'- {item.product_name} x {item.quantity} = {item.price * item.quantity} руб.\n'

    message += f'''
    Итого: {order.total_price} руб.
    Адрес доставки: {order.address}
    Статус: {order.get_status_display()}

    Спасибо за заказ!
    '''

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.user.email],
        fail_silently=True,
    )
    print(f'Email отправлен на {order.user.email}')


def send_order_notification_to_admin(order):
    """Отправка уведомления администратору о новом заказе"""
    subject = f'Новый заказ №{order.id}'
    message = f'''
    Поступил новый заказ №{order.id}

    Покупатель: {order.user.username}
    Сумма: {order.total_price} руб.
    Адрес: {order.address}

    Товары:
    '''

    for item in order.items.all():
        message += f'- {item.product_name} x {item.quantity}\n'

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=True,
    )
    print(f'Уведомление администратору отправлено')