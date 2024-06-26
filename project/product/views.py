from django.shortcuts    import render, redirect
from .models             import *
from django.contrib      import messages
from seller.models       import Store
from accounts.models     import Account, Notification
from django.http         import HttpResponse
from authenticate.views  import validate_field
from django.utils        import timezone
from customer.models     import Wishlist, Cart

def createProduct(request, store_id):
    
    categories = Category.objects.all()
    category_dict = {}
    
    account = Account.objects.get(email=request.user.email)
    
    if request.user.is_authenticated and (request.user.role == 'seller' or request.user.role == 'admin'):
        if request.method == 'POST':
            
            store   = Store.objects.get(id=store_id)
            
            name            = request.POST.get('name')
            description     = request.POST.get('description')
            price           = request.POST.get('price')
            discount        = request.POST.get('discount')
            in_stock        = request.POST.get('in_stock')
            published       = request.POST.get('published')
            brand           = request.POST.get('brand')
            model           = request.POST.get('model')
            warranty        = request.POST.get('warranty')
            
            category        = request.POST.get('category')

            errors = []
            
            validate_field(name,        "", "Product name must not be empty",        errors)
            validate_field(description, "", "Product description must not be empty", errors)
            validate_field(price,       "", "Product price must not be empty",       errors)
            validate_field(brand,       "", "Product brand must not be empty",       errors)
            validate_field(model,       "", "Product model must not be empty",       errors)
            validate_field(warranty,    "", "Product warranty must not be empty",    errors)
            validate_field(category,    "", "Product select a product category",     errors)

            if errors:
                for error in errors:
                    messages.error(request, error)
                    
                return redirect('/product/create-product/' + str(store_id))
            else:
                product = Product(
                    name        = name,
                    description = description,
                    price       = price,
                    discount    = 0 if discount == '' else discount,
                    in_stock    = True if in_stock == 'on' else False,
                    published   = True if published == 'on' else False,
                    brand       = brand,
                    model       = model,
                    warranty    = warranty,
                    account     = account,
                    store       = store
                )
                
                product.save()
                
                selected_category = Category.objects.get(name=category)
                
                productCategory = ProductCategory(category=selected_category, product=product)
                productCategory.save()
                
                messages.success(request, 'Product saved successfully')
                
                return redirect('/product/add-product-image/' + str(product.id))
        else:
            for category in categories:
                if category.parent is None:
                    if category.id not in category_dict:
                        category_dict[category.id] = {'category': category, 'children': []}
                else:
                    if category.parent.id not in category_dict:
                        category_dict[category.parent.id] = {'category': category.parent, 'children': []}
                    category_dict[category.parent.id]['children'].append(category)
            
            context = {
                'category_dict' : category_dict,
                'store_id'      : store_id,
                'page_title'    : 'Create Product',
                'referrer'      : '/seller/store/details/' + str(store_id)
            }
            
            return render(request, 'product/product_create.html', context)
    else:
        return redirect('unauthorized')

def editProduct(request, product_id):
    
    account = Account.objects.get(email=request.user.email)
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated and (request.user.role == 'seller' or request.user.role == 'admin') and product.account == account:
        if request.method == 'POST':
            
            name            = request.POST.get('name')
            description     = request.POST.get('description')
            price           = request.POST.get('price')
            discount        = request.POST.get('discount')
            in_stock        = request.POST.get('in_stock')
            published       = request.POST.get('published')
            brand           = request.POST.get('brand')
            model           = request.POST.get('model')
            warranty        = request.POST.get('warranty')
            
            category        = request.POST.get('category')

            errors = []
            
            validate_field(name,        "", "Product name must not be empty",        errors)
            validate_field(description, "", "Product description must not be empty", errors)
            validate_field(price,       "", "Product price must not be empty",       errors)
            validate_field(brand,       "", "Product brand must not be empty",       errors)
            validate_field(model,       "", "Product model must not be empty",       errors)
            validate_field(warranty,    "", "Product warranty must not be empty",    errors)
            validate_field(category,    "", "Product select a product category",     errors)

            if errors:
                for error in errors:
                    messages.error(request, error)
                    
                return redirect('/product/create-product/' + str(store_id))
            else:
                product = Product.objects.get(id=product_id)
                
                product.name        = name
                product.description = description
                product.price       = price
                product.discount    = 0 if discount == '' else discount
                product.in_stock    = True if in_stock == 'on' else False
                product.published   = True if published == 'on' else False
                product.brand       = brand
                product.model       = model
                product.warranty    = warranty
                
                product.updated_at  = timezone.now()
                
                product.save()
                
                return redirect('/product/edit-product-image/' + str(product.id))
        else:
            categories = Category.objects.all()
            category_dict = {}
            
            product_category = ProductCategory.objects.get(product=product)
            
            for category in categories:
                if category.parent is None:
                    if category.id not in category_dict:
                        category_dict[category.id] = {'category': category, 'children': []}
                else:
                    if category.parent.id not in category_dict:
                        category_dict[category.parent.id] = {'category': category.parent, 'children': []}
                    category_dict[category.parent.id]['children'].append(category)
            
            context = {
                'category_dict'    : category_dict,
                'product'          : product,
                'product_category' : product_category,
                'page_title'       : 'Edit Product',
                'referrer'         : '/seller/products'
            }
            
            return render(request, 'product/product_edit.html', context)

    else:
        return redirect('unauthorized')
    
def deleteProduct(request, product_id):
    account = Account.objects.get(email=request.user.email)
    product = Product.objects.get(id=product_id)
    
    store_id = product.store.id
    
    if request.user.is_authenticated and (request.user.role == 'seller' or request.user.role == 'admin') and product.account == account:
        
        product.delete()
        
        return redirect('/seller/store/details/' + str(store_id))
    else:
        return redirect('unauthorized')
    
def productAddImages(request, product_id):
    if request.user.is_authenticated and (request.user.role == 'seller' or request.user.role == 'admin'):
        account = Account.objects.get(email=request.user.email)
        
        product = Product.objects.get(id=product_id)
        
        galleries = Gallery.objects.all().filter(product=product).order_by('display_order')
        
        context = {
            'product_id' : product_id,
            'galleries'  : galleries,
            'edit'       : False,
        }
        
        return render(request, 'product/product_create_add_image.html', context)
            
    else:
        return redirect('unauthorized')

def productEditImages(request, product_id):
    if request.user.is_authenticated and (request.user.role == 'seller' or request.user.role == 'admin'):
        account = Account.objects.get(email=request.user.email)
        
        product = Product.objects.get(id=product_id)
        
        galleries = Gallery.objects.all().filter(product=product).order_by('display_order')
        
        context = {
            'product_id' : product_id,
            'galleries'  : galleries,
            'edit'       : True,
            'page_title' : 'Edit Product',
            'referrer'   : '/seller/store/product/details/' + product_id,
        }
        
        return render(request, 'product/product_create_add_image.html', context)
            
    else:
        return redirect('unauthorized')
   
def uploadProductImage(request, product_id):
    if request.user.is_authenticated and (request.user.role == 'seller' or request.user.role == 'admin'):
        if request.method == 'POST':

            product       = Product.objects.get(id=product_id)
            galleries     = Gallery.objects.filter(product=product)
            edit          = request.POST.get('edit')
            
            total_gallery = galleries.count()
            
            images   = request.FILES.getlist('images')

            print(images)

            if not images:
                messages.error(request, "Please select a image to upload")
                
                return redirect('/product/add-product-image/' + str(product.id))
            else:
                if total_gallery >= 5:
                    messages.error(request, 'Maximum image limit reached')
                    if edit == 'True':
                        return redirect('/product/edit-product-image/' + str(product.id))
                    else:
                        return redirect('/product/edit-product-image/' + str(product.id))
                else:
                    for image in images:
                        gallery = Gallery(product=product, image=image)
                        gallery.save()
                        
                    messages.success(request, 'Image uploaded successfully')
                        
                    if edit == 'True':
                        return redirect('/product/edit-product-image/' + str(product.id))
                    else:
                        return redirect('/product/edit-product-image/' + str(product.id))
        else:
            return HttpResponse('Inavlid request')
    
    else:
        return redirect('unauthorized')

def deleteProductImage(request, gallery_id):
    
    account = Account.objects.get(email=request.user.email)
    gallery = Gallery.objects.get(id=gallery_id)
    
    if request.user.is_authenticated and request.user.role == 'seller' and gallery.product.account == account:
        
        gallery.delete()
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')

def increaseDisplayOrder(request, gallery_id):
    
    account = Account.objects.get(email=request.user.email)
    gallery             = Gallery.objects.get(id=gallery_id)
    
    if request.user.is_authenticated and request.user.role == 'seller' and gallery.product.account == account:
        gallery.move_up()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')
    
def decreaseDisplayOrder(request, gallery_id):
    
    account = Account.objects.get(email=request.user.email)
    gallery             = Gallery.objects.get(id=gallery_id)
    
    if request.user.is_authenticated and request.user.role == 'seller' and gallery.product.account == account:
        gallery.move_down()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')

def productCreateComplete(request, product_id):
    
    account = Account.objects.get(email=request.user.email)
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated and request.user.role == 'seller' and product.account == account:
        galleries = Gallery.objects.all().filter(product=product).order_by('display_order')
            
        context = {
            'product'     : product,
            'galleries'   : galleries,
        }
        
        messages.success(request, 'Successfully saved product')
        
        return render(request, 'product/product_create_complete.html', context)
    else:
        return redirect('unauthorized')

def publishProduct(request, product_id):
    account = Account.objects.get(email=request.user.email)
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated and request.user.role == 'seller' and product.account == account:
        product.published = True
        product.save()
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')
    
def unpublishProduct(request, product_id):
    account = Account.objects.get(email=request.user.email)
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated and request.user.role == 'seller' and product.account == account:
        product.published = False
        product.save()
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')
    
def outStockProduct(request, product_id):
    account = Account.objects.get(email=request.user.email)
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated and request.user.role == 'seller' and product.account == account:
        product.in_stock = False
        product.save()
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')
        
def inStockProduct(request, product_id):
    account = Account.objects.get(email=request.user.email)
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated and request.user.role == 'seller' and product.account == account:
        product.in_stock = True
        product.save()
        
        wishlists = Wishlist.objects.filter(product=product)
        
        for wishlist in wishlists:
            notification = Notification(
                account = wishlist.account,
                title   = 'Product arrived at stock',
                content = 'Your wishlisted product ' + product.name + ' just arrived at stock. Buy now.',
                ref     = '/product/details/' + str(product.id)
            )
            notification.save()
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')
    
def addProductAttribute(request, product_id):
    account = Account.objects.get(email=request.user.email)
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated and request.user.role == 'seller' and product.account == account:
        
        name  = request.POST.get('name')
        value = request.POST.get('value')
    
        errors = []
            
        validate_field(name, "", "Please enter attribute name", errors)
    
        if errors:
            for error in errors:
                messages.error(request, error)
                
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            
            parent_attr = request.POST.get('parent_attr')
            
            if parent_attr is None or parent_attr == '':
                productAttribute = ProductAttribute(name=name, value=value, parent=None, product=product)
            else:
                parent           = ProductAttribute.objects.get(id=parent_attr)
                
                productAttribute = ProductAttribute(name=name, value=value, parent=parent, product=product)
                
            productAttribute.save()

            messages.success(request, "Successfully added attribute")
            
            return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        return redirect('unauthorized')
    
def deleteProductAttribute(request, attribute_id):
    
    account = Account.objects.get(email=request.user.email)
    attribute = ProductAttribute.objects.get(id=attribute_id)
    
    if request.user.is_authenticated and request.user.role == 'seller' and attribute.product.account == account:
        attribute.delete()
        
        messages.success(request, 'Attribute deleted successfully')
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')

def get_attribute_tree(attributes, parent=None):
        tree = []
        for attribute in attributes.filter(parent=parent):
            subtree = get_attribute_tree(attributes, parent=attribute)
            tree.append({'attribute': attribute, 'children': subtree})
        return tree

def get_category_hierarchy(category):
        hierarchy = []
        while category:
            hierarchy.insert(0, category)
            category = category.parent
        return hierarchy
        
def productDetails(request, product_id):
    
    product          = Product.objects.get(id=product_id)
    galleries        = Gallery.objects.filter(product=product).order_by('display_order')
    productAttribute = ProductAttribute.objects.filter(product=product)
    attribute_count  = productAttribute.count()
    
    attribute_tree = get_attribute_tree(productAttribute)
    
    similar_product_category = ProductCategory.objects.filter(product=product).values_list('category', flat=True)
    
    similar_products = Product.objects.filter(
        productcategory__category__in=similar_product_category
    ).exclude(id=product.id).distinct()
    
    category = ProductCategory.objects.get(product=product).category
    category_hierarchy = get_category_hierarchy(category)
    
    if not request.user.is_anonymous:
        wishlists        = Wishlist.objects.filter(product=product)
        account          = Account.objects.get(email=request.user.email)
        carts            = Cart.objects.filter(product=product)
        
        wishlist         = Wishlist.objects.filter(account=account, product=product)
            
        try:
            cart     = Cart.objects.filter(account=account)
        except Cart.DoesNotExist:
            cart = None
        
        if wishlist.count() > 0:
            is_wishlisted = True
        else:
            is_wishlisted = False
            
        if cart:
            in_cart = True
        else:
            in_cart = False
    else:
        is_wishlisted = False
        in_cart       = False

    context = {
        'galleries'          : galleries,
        'product'            : product,
        'attribute_tree'     : attribute_tree,
        'attribute_count'    : attribute_count,
        'is_wishlisted'      : is_wishlisted,
        'in_cart'            : in_cart,
        'similar_products'   : similar_products,
        'category_hierarchy' : category_hierarchy,
    }
    
    return render(request, 'product/product_details.html', context)

def reviewProduct(request):
    
    account = Account.objects.get(email=request.user.email)
    
    review_id = request.POST.get('review_id')
    rating    = request.POST.get('rating')
    
    review = Review.objects.get(id=review_id)
    
    if review.orderItem.order.customer == account: 
        review.rating = rating
        review.save()
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')
    