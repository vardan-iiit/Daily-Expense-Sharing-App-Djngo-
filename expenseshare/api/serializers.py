from rest_framework import serializers
from .models import User, Expense

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile_number']

    
class ExpenseSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'creator', 'description', 'amount', 'split_method',  'split_details','participants', 'created_at']
