from django.shortcuts               import render, redirect
from django.contrib.auth.decorators import login_required
from authenticate.decorators        import allowed_account
from accounts.countries             import countries
from .models                        import Store
from accounts.models                import Address, Account
from authenticate.views             import validate_field
from django.utils                   import timezone
from datetime                       import datetime, timedelta
from product.models                 import *
from product.views                  import get_attribute_tree
from collections                    import defaultdict
from django.db.models               import Count, Subquery, OuterRef, Sum

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['seller', 'admin'])
def dashboard(request):

    account = Account.objects.get(email=request.user.email)

    # Stores
    stores = Store.objects.all().filter(account=account)
    
    # Order Status
    orderItems = OrderItem.objects.filter(product__account=account)
    
    # Total Products
    product_count = Product.objects.filter(store__account=account).count()
    
    # Total Sale
    sell_by_day = Sell.get_current_month_sell(account)
    sells = Sell.objects.filter(orderItem__product__account=account)
    
    total_sale = 0
    item_sold = 0
    for sell in sells:
        total_sale = total_sale + sell.quantity * sell.price
        item_sold  = item_sold  + sell.quantity
        
    # Avarage rating
    reviews = Review.objects.filter(orderItem__product__account=account)
    review_count = 0
    total_rating = 0
    
    for review in reviews:
        if review.rating is not None:
            total_rating = total_rating + review.rating
            review_count = review_count + 1
    
    avarage_rating = total_rating / review_count
        
    processing = 0
    accepted   = 0
    shipped    = 0
    delivered  = 0
    
    for orderItem in orderItems:
        match orderItem.status:
            case 'processing':
                processing = processing + 1
            case 'accepted':
                accepted   = accepted + 1
            case 'shipped':
                shipped    = shipped + 1
            case 'delivered':
                delivered  = delivered + 1
    
    context = {
        'stores'             : stores,
        'page_title'         : 'Dashboard',
        'processing'         : processing,
        'accepted'           : accepted,
        'shipped'            : shipped,
        'delivered'          : delivered,
        'product_count'      : product_count,
        'order_count'        : orderItems.count(),
        'sell_by_day'        : sell_by_day, 
        'total_sale'         : total_sale,
        'avarage_rating'     : avarage_rating,
        'item_sold'          : item_sold,
    }

    return render(request, 'seller/dashboard.html', context)

# Store Index
@login_required(login_url='/auth/login')
def storeIndex(request):
    
    account = Account.objects.get(email=request.user.email)
    stores = Store.objects.all().filter(account=account)

    stores_with_product = []
    
    for store in stores:
        totalProduct = Product.objects.filter(store=store).count()
        
        stores_with_product.append({
            'store' : store,
            'totalProduct' : totalProduct
        })

    context = {
        'stores_with_product' : stores_with_product,
        'page_title'          : 'Stores',
        'referrer'            : '/seller/dashboard'
    }
    
    return render(request, 'seller/store_index.html', context)

# Create Store
@login_required(login_url='/auth/login')
def createStore(request):

    account = Account.objects.get(email=request.user.email)

    if request.method == 'POST':
        name        = request.POST.get('name')
        street      = request.POST.get('street')
        city        = request.POST.get('city')
        district    = request.POST.get('district')
        country     = request.POST.get('country')
        ref         = request.POST.get('reference')

        errors = []

        validate_field(name    ,  "", "Name cannot be empty",           errors)
        validate_field(street  ,  "", "Street name cannot be empty",    errors)
        validate_field(city    ,  "", "City name cannot be empty",      errors)
        validate_field(district,  "", "District name cannot be empty",  errors)
        validate_field(country ,  "", "Country name cannot be empty",   errors)

        if not country in countries:
            errors.append("Invalid country name. Check spelling")

        if not errors:
            account = Account.objects.get(email=request.user.email)
            address = Address(
                account  = account,
                title    = name,
                street   = street,
                city     = city,
                district = district,
                country  = country
            )

            address.save()

            store = Store(
                account = account,
                name    = name,
                address = address
            )

            store.save()

            return redirect('/seller/' + str(ref))

        else:
            # Return errors if exists
            for error in errors:
                messages.error(request, error)

    else:
        context = {
            'countries'  : countries,
            'page_title' : 'Add store',
            'referrer'   : '/seller/stores'
        }

        return render(request, 'seller/store_create.html', context)

# Store Details
@login_required(login_url='/auth/login')
def storeDetails(request, id):

    account     = Account.objects.get(email=request.user.email)
    store       = Store.objects.get(id=id)
    
    if request.user.is_authenticated and store.account == account:
        
        products    = Product.objects.all().filter(store=store)

        context = {
            'store'      : store,
            'products'   : products,
            'page_title' : 'Store Details',
            'referrer'   : '/seller/stores'
        }

        return render(request, 'seller/store_details.html', context)
    else:
        return redirect('unauthorized')

# Edit Store
@login_required(login_url='/auth/login')
def editStore(request, id):
    store   = Store.objects.get(id=id)
    account = Account.objects.get(email=request.user.email)
    address = Address.objects.get(id=store.address.id)
    
    if store.account == account:

        if request.method == "POST":
            name        = request.POST.get('name')
            street      = request.POST.get('street')
            city        = request.POST.get('city')
            district    = request.POST.get('district')
            country     = request.POST.get('country')
            ref         = request.POST.get('reference')

            errors = []

            validate_field(name    ,  "", "Name cannot be empty",           errors)
            validate_field(street  ,  "", "Street name cannot be empty",    errors)
            validate_field(city    ,  "", "City name cannot be empty",      errors)
            validate_field(district,  "", "District name cannot be empty",  errors)
            validate_field(country ,  "", "Country name cannot be empty",   errors)

            if not country in countries:
                errors.append("Invalid country name. Check spelling")

            if not errors:
                store.name       = name
                address.street   = street
                address.city     = city
                address.district = district
                address.country  = country

                address.save()

                store.address = address
                store.updated_at = timezone.now()
                
                store.save()

                return redirect('/seller/store/details/' + str(id))
        else:
            context = {
                'store'     : store,
                'countries' : countries,
                'page_title' : 'Edit store',
                'referrer'   : '/seller/store/details/' + str(id)
            }

            return render(request, 'seller/store_edit.html', context)
    else:
        return redirect('unauthorized')
    
# Delete Store
@login_required(login_url='/auth/login')
def deleteStore(request, id):
    store   = Store.objects.get(id=id)
    account = Account.objects.get(email=request.user.email)
    
    if store.account == account:
        store.delete()
        
        return redirect('/seller/dashboard')
    else:
        return redirect('unauthorized')
    
# Store Product Details
@login_required(login_url='/auth/login')
def storeProductDetails(request, product_id):
    
    account = Account.objects.get(email=request.user.email) 
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated and product.account == account:
        
        galleries = Gallery.objects.filter(product=product).order_by('display_order')
        
        attributes = ProductAttribute.objects.filter(product=product)
        
        attribute_count = attributes.count()
        
        attribute_tree = get_attribute_tree(attributes)
        
        context = {
            'product'         : product,
            'galleries'       : galleries,
            'attribute_count' : attribute_count,
            'attribute_tree'  : attribute_tree,
            'page_title'      : 'Product details',
            'referrer'        : '/seller/products'
        }
        
        return render(request, 'product/product_details_store.html', context)
    else:
        return redirect('unauthorized')
    
# Product Index
@login_required(login_url='/auth/login')
def productIndex(request):
    
    account  = Account.objects.get(email=request.user.email) 
    
    if request.user.is_authenticated and request.user.role == 'seller':
                
        filter = request.GET.get('filter')
        
        match filter:
            case 'oldest':
                products    = Product.objects.all().filter(account=account).order_by('-created_at')
            case 'popular':
                sell_quantity_subquery = Sell.objects.filter(orderItem__product=OuterRef('pk')).values('orderItem__product').annotate(total_quantity=Sum('quantity')).values('total_quantity')
    
                products = Product.objects.filter(account=account).annotate(total_sales=Subquery(sell_quantity_subquery)).order_by('-total_sales')
            case 'published':
                products    = Product.objects.all().filter(account=account).order_by('-published')
            case _:
                products    = Product.objects.all().filter(account=account).order_by('created_at')
         
        context = {
            'products'   : products,
            'page_title' : 'Products',
            'referrer'   : '/seller/dashboard'
        }

        return render(request, 'seller/products.html', context)
    else:
        return redirect('unauthorized')
    
@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['seller'])
def orders(request):
    
    account = Account.objects.get(email=request.user.email)
    
    filter_status = request.GET.get('filter')
    
    if filter_status is None:    
        order_items = OrderItem.objects.filter(product__account=account).order_by('-created_at')
    else:
        order_items = OrderItem.objects.filter(product__account=account, status=filter_status).order_by('-created_at')
    
    grouped_order_items = {}
    for order_item in order_items:
        if order_item.order.id not in grouped_order_items:
            grouped_order_items[order_item.order.id] = {
                'order': order_item.order,
                'order_items': []
            }
        grouped_order_items[order_item.order.id]['order_items'].append(order_item)
    
    context = {
        'grouped_order_items' : grouped_order_items.values(),
        'page_title'          : 'Orders',
        'referrer'            : '/seller/dashboard'
    }
    
    return render(request, 'seller/orders.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['seller'])
def orderDetails(request, order_id):
    
    account = Account.objects.get(email=request.user.email)
    
    order   = Order.objects.get(id=order_id)
    
    order_items = OrderItem.objects.filter(order=order, product__account=account)
    
    total = 0
    
    for order_item in order_items:
        total = total + ( order_item.price * order_item.quantity )
    
    context = {
        'order'       : order,
        'order_items' : order_items,
        'page_title'  : 'Order Details',
        'referrer'    : '/seller/orders',
        'total'       : total,
    }
    
    return render(request, 'seller/order_details.html', context)

def changeOrderItemStatus(request, item_id, status):
    
    account = Account.objects.get(email=request.user.email)
    order_item = OrderItem.objects.get(id=item_id)
    
    if order_item.product.account == account:
        order_item.status = status
        order_item.updated_at = timezone.now
        order_item.save()
        
        order_items = OrderItem.objects.filter(order=order_item.order)
        for item in order_items:
            item.order = order_item.order
            item.save()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')
    
    