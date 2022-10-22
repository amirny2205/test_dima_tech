from django.db import models


class ProductModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "products"


class BillModel(models.Model):
    bill_id = models.IntegerField(primary_key=True)
    balance = models.IntegerField(default=0)
    owner = models.ForeignKey("auth.User", related_name="bills", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.bill_id)

    class Meta:
        verbose_name_plural = "bills"


class TransactionModel(models.Model):
    summ = models.IntegerField()
    bill = models.ForeignKey(BillModel, related_name="transactions", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "transactions"
