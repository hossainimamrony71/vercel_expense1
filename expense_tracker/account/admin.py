from django.contrib import admin
from .models import User
from expense.models import Transaction,ExpenseCategory,ExpenseSubCategory, MoneyAllocation
# Register your models here.
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseSubCategory)
admin.site.register(MoneyAllocation)