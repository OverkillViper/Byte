from django.urls import path
from . import views
from accounts.views import addAddress, deleteAddress

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    
    # Wishlist
    path('add-to-wishlist/<str:product_id>',      views.addToWishlist,      name='addToWishlist'),
    path('remove-from-wishlist/<str:product_id>', views.removeFromWishlist, name='removeFromWishlist'),
    path('wishlist',                              views.wishlist,           name='wishlist'),
    
    # Cart
    path('cart',                           views.viewCart,           name='viewCart'),
    path('add-to-cart',                    views.addToCart,          name='addToCart'),
    path('remove-from-cart/<str:cart_id>', views.removeFromCart,     name='removeFromCart'),
    path('update-cart-quantity',           views.updateCartQuantity, name='updateCartQuantity'),
    
    # Checkout
    path('checkout', views.checkout, name='checkout'),
    
    # Address
    path('addresses',                       views.addresses, name='addresses'),
    path('add-address',                     addAddress,      name='addAddress'),
    path('delete-address/<str:address_id>', deleteAddress,   name='deleteAddress'),
    
    # Order
    path('orders',                          views.orders,           name='orders'),
    path('order/details/<str:order_id>',    views.orderDetails,     name='orderDetails'),
    path('place-order',                     views.placeOrder,       name='placeOrder'),
    path('order-complete/<str:order_id>',   views.orderComplete,    name='orderComplete'),
    path('order/delete-item/<str:item_id>', views.deleteOrderItem,  name='deleteOrderItem'),
    path('cancel-order/<str:order_id>',     views.cancelOrder,      name='cancelOrder'),
]