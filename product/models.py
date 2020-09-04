from django.db import models
from django.core.validators import MinValueValidator

import uuid

class Products(models.Model):
    # product sku
    sku_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # product name
    name = models.CharField(max_length=255, null=False)
    qty = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

    def __str__(self):
        return "{}".format(self.sku_id)
