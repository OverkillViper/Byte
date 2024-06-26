from django.shortcuts               import render, redirect
from product.models                 import *
from customer.models                import *
from product.views                  import get_attribute_tree
from django.contrib.auth.decorators import login_required
from authenticate.decorators        import allowed_account
from django.contrib                 import messages
from django.http                    import HttpResponse
from seller.models                  import Store
from accounts.models                import Account
from django.db.models               import Q, Avg, Sum, OuterRef, Subquery
from django.db                      import connection

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['admin'])
def dashboard(request):
    
    # Products
    product_count = Product.objects.all().count()
    
    # Customer
    customer_count = Account.objects.filter(role='customer').count()
    
    # Seller
    seller_count = Account.objects.filter(role='seller').count()
    
    # Stores
    store_count = Store.objects.all().count()
    
    # Sales
    sells = Sell.objects.all()
    sell_by_day = Sell.get_current_month_sell(request.user)
    sell_count = 0
    
    for sell in sells:
        sell_count = sell_count + sell.quantity
    
    # Wishlists
    wishlist_count = Wishlist.objects.all().count
    
    # Payment count
    cash_payment = Order.objects.filter(payment='cod').count()
    cashless_payment = Order.objects.filter(payment='cashless').count()
    
    # Top Stores
    sell_quantity_subquery = Sell.objects.filter(orderItem__product__store=OuterRef('pk')).values('orderItem__product__store').annotate(total_quantity=Sum('quantity')).values('total_quantity')

    top_stores = Store.objects.all().annotate(total_sales=Subquery(sell_quantity_subquery)).order_by('-total_sales')[:3]

    top_stores_with_total_sale = []
    
    for store in top_stores:
        total_sale = Sell.objects.filter(orderItem__product__store=store).aggregate(total_quantity=Sum('quantity'))

        top_stores_with_total_sale.append({
            'store'      : store,
            'total_sale' : total_sale
        })
    
    context = {
        'page_title'        : 'Dashbaord',
        'product_count'     : product_count,
        'customer_count'    : customer_count,
        'seller_count'      : seller_count,
        'store_count'       : store_count,
        'sell_count'        : sell_count,
        'wishlist_count'    : wishlist_count,
        'cash_payment'      : cash_payment,
        'cashless_payment'  : cashless_payment,
        'sell_by_day'       : sell_by_day,
        'top_stores'        : top_stores_with_total_sale
    }
    
    return render(request, 'moderator/dashboard.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['admin'])
def categories(request):
    
    categories = Category.objects.all()
    
    category_tree = get_attribute_tree(categories)
    
    context = {
        'page_title'    : 'Categories',
        'referrer'      : '/moderator/dashboard',
        'category_tree' : category_tree,
        'categories'    : categories,
    }
    
    return render(request, 'moderator/categories.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['admin'])
def addCategory(request):
    
    if request.method == 'POST':
        parent_id = request.POST.get('parent_category')
        name      = request.POST.get('name')
        
        print(parent_id)
        
        if parent_id is None or parent_id == '':
            category = Category(name=name)
        else:
            parent = Category.objects.get(id=parent_id)
            
            category = Category(name=name, parent=parent)
            
        category.save()
        
        messages.success(request, 'Category created successfully')
    
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid request')
    
    
@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['admin'])
def deleteCategory(request, category_id):
    
    category = Category.objects.get(id=category_id)
    category.delete()
    
    messages.success(request, 'Category deleted successfully')
    
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['admin'])
def moderatorStores(request):
    
    query = request.GET.get('search', '')  # Get the search query from the request

    if query:
        stores = Store.objects.filter(
            Q(name__icontains=query) |
            Q(account__first_name__icontains=query) |
            Q(account__last_name__icontains=query) |
            Q(address__street__icontains=query) |
            Q(address__city__icontains=query) |
            Q(address__district__icontains=query) |
            Q(address__country__icontains=query)
        )
    else:
        stores = Store.objects.all()
    
    context = {
        'page_title'    : 'Stores',
        'referrer'      : '/moderator/dashboard',
        'stores'        : stores,
    }
    
    return render(request, 'moderator/stores.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['admin'])
def moderatorStoresDetails(request, store_id):
    
    store = Store.objects.get(id=store_id)
    
    products = Product.objects.filter(store=store)
    
    context = {
        'page_title'   : 'Stores',
        'referrer'     : '/moderator/stores',
        'store'        : store,
        'products'     : products,
    }
    
    return render(request, 'moderator/store_details.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['admin'])
def accounts(request):
    
    query = request.GET.get('search', '')  # Get the search query from the request

    if query:
        accounts = Account.objects.all().exclude(role='admin').filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(first_name__icontains=query.split(' ')[0], last_name__icontains=query.split(' ')[-1]) |
            Q(last_name__icontains=query.split(' ')[0], first_name__icontains=query.split(' ')[-1])
        )
    else:
        accounts = Account.objects.all().exclude(role='admin')
    
    context = {
        'page_title'   : 'Accounts',
        'referrer'     : '/moderator/dashboard',
        'accounts'     : accounts
    }
    
    return render(request, 'moderator/accounts.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['admin'])
def moderatorProducts(request):
    
    query = request.GET.get('search', '')  # Get the search query from the request

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(price__icontains=query)
        )
    else:
        products = Product.objects.all().order_by('-created_at')
    
    context = {
        'page_title'   : 'Products',
        'referrer'     : '/moderator/dashboard',
        'products'     : products
    }
    
    return render(request, 'moderator/products.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['admin'])
def accountDetails(request, account_id):
    
    account = Account.objects.get(email=account_id)
    
    if account.role == 'customer':
        orders           = OrderItem.objects.filter(order__customer=account).exclude(status='delivered').count()
        products_bought  = Sell.objects.filter(customer=account).count()
        
        product_count    = 0
        sales            = 0
        average_rating   = 0
        stores           = 0
            
    elif account.role == 'seller':
        orders           = 0
        products_bought  = 0

        product_count = Product.objects.filter(account=account).count()
        sales         = Sell.objects.filter(seller=account).count()
        reviews       = Review.objects.filter(orderItem__product__account=account)
        stores        = Store.objects.filter(account=account).count()
        
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        average_rating = average_rating if average_rating is not None else 0
        
    else:
        pass
    
    context = {
        'account'         : account,
        'page_title'      : 'Account Details',
        'referrer'        : '/moderator/accounts',
        'orders'          : orders,
        'products_bought' : products_bought,
        'product_count'   : product_count,
        'sales'           : sales,
        'average_rating'  : average_rating,
        'stores'          : stores,
    }
    
    return render(request, 'moderator/account_details.html', context)