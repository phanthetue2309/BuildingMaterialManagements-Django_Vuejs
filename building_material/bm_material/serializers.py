from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'address', 'phone_number', 'discription']
