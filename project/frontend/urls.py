from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('stores', views.stores, name='stores'),
    path('store/<str:store_id>', views.storeDetails, name='storeDetails'),
    path('products', views.products, name='products'),
    path('categories', views.categories, name='categories'),
    path('category/<str:category_id>', views.category, name='category'),
]