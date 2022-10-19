from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()


class Bill(models.Model):
    bill_id = models.IntegerField(primary_key=True)
    balance = models.IntegerField(default=0)
    user = models.ForeignKey('auth.User', related_name="bills", on_delete=models.CASCADE)


class Transaction(models.Model):
    summ = models.IntegerField()
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
