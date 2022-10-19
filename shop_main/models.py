from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.title


class Bill(models.Model):
    bill_id = models.IntegerField(primary_key=True)
    balance = models.IntegerField(default=0)
    user = models.ForeignKey("auth.User", related_name="bills", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.bill_id)


class Transaction(models.Model):
    summ = models.IntegerField()
    bill = models.ForeignKey(Bill, related_name="transactions", on_delete=models.CASCADE)
