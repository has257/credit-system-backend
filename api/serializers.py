from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'age', 'monthly_income', 
                  'phone_number', 'approved_limit', 'current_debt']
        read_only_fields = ['id', 'approved_limit', 'current_debt']

