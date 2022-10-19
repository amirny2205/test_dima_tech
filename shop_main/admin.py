from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from django.contrib.auth.models import User
from shop_main.models import *

admin.site.register(Product)
admin.site.register(Bill)
admin.site.register(Transaction)

class BillInline(admin.TabularInline):
    model = Bill
    fk_name = 'user'

class CustomUserAdmin(admin.ModelAdmin):
    inlines= (
        BillInline,
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)