from django.db          import models
from hashid_field       import HashidAutoField
from accounts.models    import Account
from product.models     import Product

# Create your models here.
class Wishlist(models.Model):
    
    id          = HashidAutoField(primary_key=True)
    account     = models.ForeignKey(Account, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.name
    
class Cart(models.Model):
    
    id          = HashidAutoField(primary_key=True)
    account     = models.ForeignKey(Account, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity    = models.IntegerField(default=1)
    
    def __str__(self):
        return self.product.name