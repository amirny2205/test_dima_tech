"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from shop.views import *
from users.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>', activation_view, name='activation'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('self_info/', GetSelfInfoAPIView.as_view(), name='get self info'),
    path('buy/', BuyAPIView.as_view(), name='buy'),
    path('payment/webhook/', DepositAPIView.as_view(), name='deposit'),
]