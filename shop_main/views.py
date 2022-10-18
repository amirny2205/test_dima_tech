from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail



# def send_mail_endpoint(request):
#     print('sending email')
#     x = send_mail(
#         'Subject here',
#         'Here is the message.',
#         'amirny2205@yandex.ru',
#         ['amirny2205@yandex.ru'],
#         fail_silently=False,
#     )
#     print(x)
#     print('test')
#     return HttpResponse(x)