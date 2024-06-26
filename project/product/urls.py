from django.urls import path
from . import views

urlpatterns = [

    # Product Frontend
    path('details/<str:product_id>', views.productDetails, name='productDetails'),

    # Product CRUD
    path('create-product/<str:store_id>', views.createProduct, name='createProduct'),
    path('edit-product/<str:product_id>', views.editProduct, name='editProduct'),
    path('delete-product/<str:product_id>', views.deleteProduct, name='deleteProduct'),
    path('complete/<str:product_id>', views.productCreateComplete, name='productCreateComplete'),
    
    # Product Image CRUD
    path('add-product-image/<str:product_id>', views.productAddImages, name='productAddImages'),
    path('edit-product-image/<str:product_id>', views.productEditImages, name='productEditImages'),
    path('upload-image/<str:product_id>', views.uploadProductImage, name='uploadProductImage'),
    path('delete-image/<str:gallery_id>', views.deleteProductImage, name='deleteProductImage'),
    
    path('increaseDisplayOrder/<str:gallery_id>', views.increaseDisplayOrder, name='increaseDisplayOrder'),
    path('decreaseDisplayOrder/<str:gallery_id>', views.decreaseDisplayOrder, name='decreaseDisplayOrder'),
    
    # Product Publish
    path('publish/<str:product_id>', views.publishProduct, name='publishProduct'),
    path('unpublish/<str:product_id>', views.unpublishProduct, name='unpublishProduct'),
    
    # Product Stock
    path('out-stock/<str:product_id>', views.outStockProduct, name='outStockProduct'),
    path('in-stock/<str:product_id>', views.inStockProduct, name='inStockProduct'),
    
    # Product Attribute
    path('add-attribute/<str:product_id>', views.addProductAttribute, name='addProductAttribute'),
    path('delete-attribute/<str:attribute_id>', views.deleteProductAttribute, name='deleteProductAttribute'),
    
    # Product Rating
    path('review', views.reviewProduct, name="reviewProduct")
]