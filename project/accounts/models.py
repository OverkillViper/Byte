from django.db                  import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers                  import AccountManager
from django.utils               import timezone
from django.conf                import settings
from datetime                   import timedelta
from hashid_field               import HashidAutoField

import pytz

# Create your models here.
class Account(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('customer', 'customer'),
        ('seller',   'seller'  ),
        ('admin',    'admin'   ),
    )
    
    email       = models.EmailField(unique=True)
    role        = models.CharField(max_length=50, choices=ROLES, default='customer')
    first_name  = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    phone       = models.CharField(max_length=20, default='', blank=True)
    
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    email_verified  = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = AccountManager()

    def get_short_name(self):
        return self.email
    
    def get_role(self):
        return self.role

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.first_name + ' ' +self.last_name
    
class AccountActivationToken(models.Model):
    
    id         = HashidAutoField(primary_key=True)
    account    = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    uid        = models.CharField(max_length=255, unique=True)
    token      = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        current_time = timezone.now().astimezone(pytz.timezone('Etc/GMT-6'))
        expiration_time = self.created_at + timedelta(seconds=settings.EMAIL_VERIFY_TOKEN_TIMEOUT)
        expiration_time = expiration_time.astimezone(pytz.timezone('Etc/GMT-6'))
        return current_time >= expiration_time
    
    def __str__(self):
        return self.uid
    
class Address(models.Model):
    
    id         = HashidAutoField(primary_key=True)
    account    = models.ForeignKey(Account, on_delete=models.CASCADE)
    title      = models.CharField(max_length=100)
    street     = models.CharField(max_length=100)
    city       = models.CharField(max_length=100)
    district   = models.CharField(max_length=100)
    country    = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_address(self):
        return self.street + ', ' + self.city + ', ' + self.district + ', ' + self.country
    
class Notification(models.Model):
    
    id         = HashidAutoField(primary_key=True)
    account    = models.ForeignKey(Account, on_delete=models.CASCADE)
    title      = models.CharField(max_length=100)
    content    = models.CharField(max_length=255, null=True)
    ref        = models.CharField(max_length=100, null=True)
    seen       = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
class Conversation(models.Model):
    
    id           = HashidAutoField(primary_key=True)
    participants = models.ManyToManyField(Account, related_name='conversations')

    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ", ".join([user.get_full_name for user in self.participants.all()])
    
    def last_message(self):
        return self.messages.order_by('-created_at').first()
    
class Message(models.Model):
    
    id              = HashidAutoField(primary_key=True)
    conversation    = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender          = models.ForeignKey(Account, related_name='sent_messages', on_delete=models.CASCADE)
    content         = models.TextField()
    
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender}'