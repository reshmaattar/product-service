import json
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Products
from .serializers import ProductsSerializer

# tests for views
class BaseViewTest(APITestCase):

    client = APIClient()
    list_create_url =reverse("products-list-create")
    
    def list_url(self,filters=None):
        if filters is None:
            return self.list_create_url
        else:
            return self.list_create_url + "?" + urlencode(filters)

    def product_detail_url(self,sku_id):
        return reverse(
                    "products-detail",
                    kwargs={
                        "sku_id": sku_id
                    }
                )

    @staticmethod
    def create_product_data(name="",qty=0,price=0.00):
        
        if name != "":
            product = Products.objects.create(name=name, qty=qty,price=price)
            
    """
    Ignore keys which not to be asserted
    """
    @staticmethod
    def ignore_keys(original, *args):
        
        d = original
        
        for k in args:
            try:
                del d[k]
            except KeyError:
               pass 
        return d

    def get_all_products(self,filters=None):
        if filters is None:
            return self.client.get(self.list_create_url)
        else:
            return self.client.get(self.list_create_url,filters)

    def create_a_product(self,data):
        return self.client.post(self.list_create_url,
                data=json.dumps(data),
                content_type='application/json'
            )

    def update_a_product(self,sku_id,data):
        return self.client.put(self.product_detail_url(sku_id),
                data=json.dumps(data),
                content_type='application/json'
            )

    def fetch_a_product(self, sku_id=0):
    
        return self.client.get(self.product_detail_url(sku_id))

    def delete_a_product(self, sku_id=0):
        return self.client.delete(self.product_detail_url(sku_id))
        
    
    def setUp(self):
        
        # add test data
        self.create_product_data("Skirt",0,10.00)
        self.create_product_data("Pants",5,20.00)
        self.create_product_data("Pen set",12,5.00)
        self.create_product_data("notebook",12,10.00)
        
        
        self.valid_data = {
            "name": "test iitem",
            "qty": 2,
            "price": 10.50
        }
        self.invalid_data = {
            "name": ""
        }
        self.valid_product_id = Products.objects.first().sku_id
        self.invalid_product_id = "c4507a0a-6da6-4507-8906-0ebb1f7273ab"


class GetAllProductsTest(BaseViewTest):

    def test_get_all_products(self):

        # hit the API endpoint
        response = self.get_all_products()

        # fetch the data from db
        expected = Products.objects.all()
        serialized = ProductsSerializer(expected, many=True)
        self.assertListEqual(response.data.get('results'), serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_filter_with_instock_prducts(self):

       # hit the API endpoint
        response = self.get_all_products(filters={'in_stock':True})

        # fetch the data from db
        expected = Products.objects.filter(qty__gt=0)
        serialized = ProductsSerializer(expected, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data.get('results'), serialized.data)
        
    def test_filter_with_soldout_prducts(self):

       # hit the API endpoint
        response = self.get_all_products(filters={'in_stock':False})

        # fetch the data from db
        expected = Products.objects.filter(qty=0)
        serialized = ProductsSerializer(expected, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data.get('results'), serialized.data)

class GetASingleProductTest(BaseViewTest):

    def test_valid_get_a_product(self):
        """
        This test ensures that a single product of a given id is
        returned
        """
        
        # hit the API endpoint
        response = self.fetch_a_product(self.valid_product_id)
        
        # fetch the data from db
        expected = Products.objects.get(sku_id=self.valid_product_id)
        serialized = ProductsSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_get_product(self):
        # test with a product that does not exist
        response = self.fetch_a_product(self.invalid_product_id)
        self.assertEqual(
            response.data["message"],
            "Product with id: c4507a0a-6da6-4507-8906-0ebb1f7273ab does not exist"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddProductsTest(BaseViewTest):

    def test_valid_create_a_product(self):
        """
        This test ensures that a single product can be added
        """
        
        # hit the API endpoint
        response = self.create_a_product(data=self.valid_data)
        expected_data= {**self.valid_data,
                        **{'price':"{:.2f}".format(self.valid_data['price'])}
                        }
        
        actual_data = self.ignore_keys(response.data,"sku_id")
        self.assertEqual(actual_data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_product(self):
        # test with invalid data
        response = self.create_a_product(data=self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        invalid_qty = {
            "name": "valid short","qty": -1,"price":20}
        response = self.create_a_product(data=invalid_qty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        invalid_price = {
            "name": "valid short","qty": 1,"price":"20qq"}
        response = self.create_a_product(data=invalid_price)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class UpdateProductsTest(BaseViewTest):

    def test_valid_update_a_product(self):
        
        # hit the API endpoint
        previous_data = self.fetch_a_product(self.valid_product_id).data
        response = self.update_a_product(self.valid_product_id,data=self.valid_data)
        self.assertEqual(response.data['name'], previous_data['name'])
        self.assertEqual(response.data['price'], previous_data['price']) 
        self.assertEqual(response.data['qty'], self.valid_data['qty'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_a_product(self):
            
        # test with invalid data
        response = self.update_a_product(sku_id=self.invalid_product_id,data=self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteProductsTest(BaseViewTest):

    def test_delete_a_product(self):
       
        # hit the API endpoint
        response = self.delete_a_product(self.valid_product_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # test with invalid data
        response = self.delete_a_product(self.invalid_product_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

