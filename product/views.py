from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from rest_framework.response import Response
from rest_framework.views import status
from .schema import product
from .decorators import validate_json
from .models import Products
from .serializers import ProductsSerializer


class ProductFilter(filters.FilterSet):
    in_stock = filters.BooleanFilter(field_name="qty", method='get_in_stock',label='in_stock')
    
    def get_in_stock(self, queryset, field_name, value):
        if value is True:
            res=queryset.filter(qty__gte=1)
        else:
            res = queryset.filter(qty=0)
        return res

    class Meta:
        model = Products
        fields = ['name', 'qty']

class ListCreateProductsView(generics.ListCreateAPIView):
    """
    GET products/
    POST products/
    """
    filter_class = ProductFilter
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [DjangoFilterBackend]
    

    @validate_json(schema=product)
    def post(self, request, *args, **kwargs):
        a_product = Products.objects.create(
            name=request.data["name"],
            qty=request.data["qty"],
            price=request.data["price"]
        )
        return Response(
            data=ProductsSerializer(a_product).data,
            status=status.HTTP_201_CREATED
        )


class ProductsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET products/:id/
    PUT products/:id/
    DELETE products/:id/
    """
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            a_product = self.queryset.get(sku_id=kwargs["sku_id"])
            return Response(ProductsSerializer(a_product).data)
        except Products.DoesNotExist:
            return Response(
                data={
                    "message": "Product with id: {} does not exist".format(kwargs["sku_id"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_json(schema=product)
    def put(self, request, *args, **kwargs):
        try:
            a_product = self.queryset.get(sku_id=kwargs["sku_id"])
            serializer = ProductsSerializer()
            updated_product = serializer.update(a_product, request.data)
            return Response(ProductsSerializer(updated_product).data)
        except Products.DoesNotExist:
            return Response(
                data={
                    "message": "Product with id: {} does not exist".format(kwargs["sku_id"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_product = self.queryset.get(sku_id=kwargs["sku_id"])
            a_product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Products.DoesNotExist:
            return Response(
                data={
                    "message": "Product with id: {} does not exist".format(kwargs["sku_id"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
