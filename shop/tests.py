from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from shop.models import BillModel, ProductModel

client = APIClient()


class ShopTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="user_01")
        client.force_authenticate(self.user)
        self.prod01 = ProductModel.objects.create(title="prod 01", price=100)

    def test_product_list(self):
        response = client.get(reverse('product_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_self_info(self):
        response = client.get(reverse('get self info'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_BuyAPIView_buy(self):
        bill = BillModel.objects.create(bill_id=1111, balance=200, owner=self.user)
        response = client.post(reverse('buy'), data={'product_id': self.prod01.id, 'bill_id': bill.bill_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_BuyAPIView_insufficient(self):
        bill = BillModel.objects.create(bill_id=1111, balance=60, owner=self.user)
        response = client.post(reverse('buy'), data={'product_id': self.prod01.id, 'bill_id': bill.bill_id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


