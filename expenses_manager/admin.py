from django.contrib import admin
from expenses_manager import models


admin.site.register(models.Account)
admin.site.register(models.Tag)
admin.site.register(models.Wallet)
admin.site.register(models.ExpenseCategory)
admin.site.register(models.Expense)
