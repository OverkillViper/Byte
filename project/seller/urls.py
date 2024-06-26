from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('products', views.productIndex, name='productIndex'),
    
    # Stores
    path('stores', views.storeIndex, name='storeIndex'),
    path('create-store', views.createStore, name='createStore'),
    path('store/details/<str:id>', views.storeDetails, name='storeDetails'),
    path('store/edit/<str:id>', views.editStore, name='editStore'),
    path('store/delete/<str:id>', views.deleteStore, name='deleteStore'),
    path('store/product/<str:product_id>', views.storeProductDetails, name='storeProductDetails'),
    
    # Orders
    path('orders', views.orders, name='orders'),
    path('order/details/<str:order_id>', views.orderDetails, name='orderDetails'),
    path('order/change-item-status/<str:item_id>/<str:status>', views.changeOrderItemStatus, name='changeOrderItemStatus'),
    
]