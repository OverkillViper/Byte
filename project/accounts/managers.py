from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class AccountManager(BaseUserManager):
    
    def create_user(
        self,
        email,
        password,
        first_name,
        last_name,
        phone,
        role,
    ):
        if not email:
            raise ValueError("Please provide an email")
        
        email   = self.normalize_email(email)
        account = self.model(
            email       = email,
            first_name  = first_name,
            last_name   = last_name,
            phone       = phone,
            role        = role,
        )
        
        account.set_password(password)
        account.is_staff        = False
        account.is_superuser    = False
        account.is_active       = True
        account.email_verified  = False
        
        account.save(using=self._db)
        
        return account
    
    def create_superuser(
        self,
        email,
        password,
        first_name,
        last_name,
    ):
        superuser = self.create_user(
            email      = email,
            password   = password,
            first_name = first_name,
            last_name  = last_name,
            phone      = 'N/A',
            role       = 'admin'
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.email_verified  = True
        superuser.save(using=self._db)

        return superuser
    
    def get_by_natural_key(self, email_):
        return self.get(email=email_)