from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Account)
admin.site.register(AccountActivationToken)
admin.site.register(Address)
admin.site.register(Notification)