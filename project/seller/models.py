from django.db          import models
from hashid_field       import HashidAutoField
from accounts.models    import Account, Address

# Create your models here.
class Store(models.Model):
    
    id          = HashidAutoField(primary_key=True)
    account     = models.ForeignKey(Account, on_delete=models.CASCADE)
    name        = models.CharField(max_length=255)
    address     = models.ForeignKey(Address, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name