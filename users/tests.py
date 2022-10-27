from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.conf import settings
from Crypto.Hash import SHA1
client = APIClient()


class UserTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="user_01")
        client.force_authenticate(self.user)

    def test_Deposit(self):
        transaction_id = 123321
        user_id = self.user.id
        bill_id = 123666
        amount = 200
        signature = SHA1.new()
        signature.update(f'{settings.PRIVATE_KEY}:{transaction_id}:{user_id}:{bill_id}:{amount}'.encode())
        signature = signature.hexdigest()
        response = client.post(reverse('deposit'), data={'signature': signature, 'transaction_id': transaction_id,
                                                         'user_id': user_id, 'bill_id': bill_id, 'amount': amount})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
