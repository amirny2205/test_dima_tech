from django.contrib import admin
from django.contrib.auth.models import User
from shop.models import *

admin.site.register(ProductModel)
admin.site.register(BillModel)
admin.site.register(TransactionModel)


class BillInline(admin.TabularInline):
    model = BillModel
    fk_name = 'owner'


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = (
        BillInline,
    )
