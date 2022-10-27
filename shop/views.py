from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import ProductModel
from shop.serializers import *


class ProductList(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )


class BuyAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        product_id = int(request.data['product_id'])
        product = get_object_or_404(ProductModel.objects.all(), id=product_id)
        user_bills = [b.bill_id for b in request.user.bills.all()]
        bill_id = int(request.data['bill_id'])
        if bill_id in user_bills:
            bill = BillModel.objects.get(bill_id=bill_id)
            if bill.balance >= product.price:
                TransactionModel.objects.create(bill=bill, summ=-product.price)
                bill.balance -= product.price
                bill.save()
                return Response({'detail':'success'})
            else:
                return Response({'detail':'insufficient money'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail':'wrong bill id'}, status=status.HTTP_400_BAD_REQUEST)
