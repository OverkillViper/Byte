from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    
    # Accounts
    path('accounts', views.accounts, name='accounts'),
    path('account/details/<str:account_id>', views.accountDetails, name='accountDetails'),
    
    # Stores
    path('stores', views.moderatorStores, name='moderatorStores'),
    path('store/details/<str:store_id>', views.moderatorStoresDetails, name='moderatorStoresDetails'),
    
    # Catagories
    path('categories', views.categories, name='categories'),
    path('add-category', views.addCategory, name='addCategory'),
    path('delete-category/<str:category_id>', views.deleteCategory, name='deleteCategory'),
    
    # Products
    path('products', views.moderatorProducts, name='moderatorProducts'),
]