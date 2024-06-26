from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Gallery)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(ProductAttribute)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Sell)
admin.site.register(Review)