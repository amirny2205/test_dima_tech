from rest_framework import serializers
from shop_main.models import *
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.conf import settings
from djoser.serializers import UserSerializer



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'



# class UserRegistrationSerializer(BaseUserRegistrationSerializer):
#     def create(self, validated_data):
#         try:
#             user = self.perform_create(validated_data)
#         except IntegrityError:
#             self.fail("cannot_create_user")
#         Bill.objects.create(bill_id=Bill.generate_id, user=user)
#         return user

class UserSerializerCustom(UserSerializer):
    bills = BillSerializer(many=True)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'bills',
        )
        read_only_fields = (settings.LOGIN_FIELD,)


