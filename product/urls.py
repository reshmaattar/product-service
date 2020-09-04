from django.urls import path
from .views import ListCreateProductsView, ProductsDetailView


urlpatterns = [
    path('products/', ListCreateProductsView.as_view(), name="products-list-create"),
    path('products/<uuid:sku_id>/', ProductsDetailView.as_view(), name="products-detail")
    
]
