from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Products


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
    
    def update(self, instance, validated_data):
        instance.qty = validated_data.get("qty", instance.qty)
        instance.save()
        return instance
