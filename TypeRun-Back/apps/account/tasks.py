from django.core.mail import send_mail 
from django.utils.html import format_html 
from celery import shared_task 

@shared_task()
def send_activation_email(email, code):
    activation_url = f'http://localhost:8000/api/account/activate/?u={code}'
    html_message = format_html('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Активация аккаунта</title>
        </head>
        <body>
            <p>Здравствуйте!</p>
            <p>Для активации вашего аккаунта перейдите по следующей ссылке:</p>
            <a href="{}">{}</a>
            <p>Спасибо!</p>
        </body>
        </html>
    ''', activation_url, 'Activate Account')

    send_mail(
        'Активируйте ваш аккаунт!',
        '',
        'killer@gmail.com',
        [email],
        fail_silently=False,
        html_message=html_message,
    )