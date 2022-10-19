from django.contrib import admin
from django.urls import path, re_path, include
from shop_main.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>', activation, name='activation'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('self_info/', GetSelfInfo.as_view(), name='get self info'),
    path('buy/', Buy.as_view(), name='buy'),
    path('payment/webhook/', Deposit.as_view(), name='deposit'),
]
