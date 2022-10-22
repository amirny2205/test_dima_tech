from rest_framework import serializers
from shop.models import *



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = '__all__'


class BillSerializerForUserS(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = BillModel
        fields = ['bill_id', 'balance', 'transactions']
