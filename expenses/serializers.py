from rest_framework import serializers
from .models import Expenses

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Expenses
        fields = ["id", "date", "description", "amount", "category"]