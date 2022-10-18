from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail
import requests
import shop.settings

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


def activation(request, uid, token):
    '''
    this is a workaround for user activation, because we have no frontend.
    auth/users/ creates a user and sends an activation link (defined by DJOSER['ACTIVATION_URL']) to user's email.
    Then documentation(https://djoser.readthedocs.io/en/latest/base_endpoints.html#user-activate) says:
    you should provide site in your frontend application (configured by ACTIVATION_URL)
    which will send POST request to activate endpoint.
    '''
    activation_endpoint = 'auth/users/activation/'
    port = ':' + shop.settings.SELF_PORT if shop.settings.SELF_PORT else ''
    url = shop.settings.SELF_HOST + port + '/' + activation_endpoint
    print(url)
    print(type(url))
    requests.post(url, data={'uid':uid,'token':token})
    return HttpResponse('successfully activated account!')