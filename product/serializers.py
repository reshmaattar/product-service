from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Products


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.qty = validated_data.get("qty", instance.qty)
        instance.price = validated_data.get("price", instance.price)
        instance.save()
        return instance
