from django.shortcuts               import render, redirect
from django.contrib.auth.decorators import login_required
from authenticate.decorators        import allowed_account
from .models                        import *
from product.models                 import *
from accounts.models                import Account, Notification
from django.http                    import HttpResponse
from django.contrib                 import messages
from accounts.countries             import countries
from accounts.models                import Address
from authenticate.views             import validate_field
from collections                    import defaultdict

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer', 'admin'])
def dashboard(request):
    
    page_title = 'Dashboard'
    
    account = Account.objects.get(email=request.user.email)
    
    standing_orders = Order.objects.filter(customer=account).exclude(status='delivered').count()
    completed_orders = Order.objects.filter(customer=account, status='delivered').count()

    sells = Sell.objects.filter(customer=account)
    item_bought = 0
    for sell in sells:
        item_bought = item_bought + sell.quantity
    
    cash_payment     = Order.objects.filter(customer=account, payment='cod').count()
    cashless_payment = Order.objects.filter(customer=account, payment='cashless').count()
    
    wishlist = Wishlist.objects.filter(account=account).count()
    
    money_spent = 0
    for sell in sells:
        money_spent = money_spent + sell.price
    
    total_address = Address.objects.filter(account=account).count()
    
    sell_by_day = Sell.get_current_month_sell(request.user)
    
    context = {
        'page_title'       : page_title,
        'standing_orders'  : standing_orders,
        'completed_orders' : completed_orders,
        'item_bought'      : item_bought,
        'cash_payment'     : cash_payment,
        'cashless_payment' : cashless_payment,
        'wishlist'         : wishlist,
        'money_spent'      : money_spent,
        'total_address'    : total_address,
        'sell_by_day'      : sell_by_day,
    }
    
    return render(request, 'customer/dashboard.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer'])
def addToWishlist(request, product_id):
    
    if request.user.is_authenticated and request.user.role == 'customer':   
        product = Product.objects.get(id=product_id)
        account = Account.objects.get(email=request.user.email)
        
        wishlists = Wishlist.objects.filter(product=product)
        
        try:
            wishlist = wishlists.get(account=account)
            messages.error(request, 'Product is already on your wishlist')
        except Wishlist.DoesNotExist:
            new_wishlist = Wishlist(product=product, account=account)
            new_wishlist.save()
            
            messages.success(request, 'Successfully added to your wishlist')
           
        return redirect('/product/details/' + product_id)
        
    else:
        return redirect('unauthorized')
    
@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer'])
def removeFromWishlist(request, product_id):
    
    account  = Account.objects.get(email=request.user.email)
    product  = Product.objects.get(id=product_id)
    wishlists = Wishlist.objects.filter(product=product)
    wishlist = wishlists.get(account=account)
    
    if request.user.is_authenticated:
        wishlist.delete()
        
        messages.success(request, 'Successfully removed from your wishlist')
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer'])
def addToCart(request):
    
    if request.user.is_authenticated and request.user.role == 'customer':
        
        product_id = request.GET.get('product_id')
           
        product = Product.objects.get(id=product_id)
        account = Account.objects.get(email=request.user.email)
        
        quantity = request.GET.get('quantity')
        
        existing_cart = Cart.objects.filter(account=account, product=product)
        
        if existing_cart.count() > 0:
            cart = Cart.objects.filter(account=account).get(product=product)
            cart.quantity = cart.quantity + 1
            cart.save()
        else:
            cart = Cart(product=product, account=account, quantity=quantity)
            cart.save()
        
        messages.success(request, 'Successfully added to your cart')
        
        return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        return redirect('unauthorized')

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer']) 
def viewCart(request):
        
    account = Account.objects.get(email=request.user.email)
    
    carts = Cart.objects.filter(account=account)
    
    context = {
        'carts' : carts,
    }
    
    return render(request, 'customer/cart.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer']) 
def updateCartQuantity(request):
    
    cart_id = request.POST.get('cart_id')
    cart = Cart.objects.get(id=cart_id)
    account = Account.objects.get(email=request.user.email)
    
    if request.method == 'POST' and cart.account == account:
        
        quantity = request.POST.get('quantity')
        cart.quantity = quantity
        cart.save()
        
        messages.success(request, 'Quantity updated successfully')
    
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')
    
def removeFromCart(request, cart_id):
    
    account = Account.objects.get(email=request.user.email)
    cart = Cart.objects.get(id=cart_id)
    
    if cart.account == account:
        cart.delete()
        
        messages.success(request, 'Product removed from cart')
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')
    
@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer']) 
def checkout(request):
    
    account = Account.objects.get(email=request.user.email)
    
    carts  = Cart.objects.filter(account=account)
    addressess  = Address.objects.filter(account=account)

    total_item = 0
    total_amount = 0
    
    if carts.count() < 1:
        messages.error(request, 'There is no item on your cart')
        
        return redirect('/customer/cart')
    else:
        for item in carts:
            total_item      = total_item + item.quantity
            total_amount    = total_amount + item.quantity * item.product.discounted_price()
            
        context = {
            'carts'        : carts,
            'total_item'   : total_item,
            'total_amount' : total_amount,
            'countries'    : countries,
            'addressess'   : addressess,
        }
    
        return render(request, 'customer/checkout.html', context)
    
@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer']) 
def placeOrder(request):
    
    if request.method == 'POST':
        
        address_id = request.POST.get('address')
        payment    = request.POST.get('payment')
        
        errors = []
        
        validate_field(address_id, "", "Please select delivery address", errors)
        
        if not errors:
            account     = Account.objects.get(email=request.user.email)
            address     = Address.objects.get(id=address_id)
            cart_items  = Cart.objects.filter(account=account)
            
            order       = Order(
                customer    = account,
                status      = 'processing',
                address     = address,
                payment     = payment,
            )
            
            order.save()

            seller_items = defaultdict(list)

            # Convert each cart item into order item
            for item in cart_items:
                orderItem = OrderItem(
                    product  = item.product,
                    order    = order,
                    quantity = item.quantity,
                    price    = item.product.discounted_price() * item.quantity
                )
                
                orderItem.save()
                
                # Get sellers of products
                seller = item.product.account
                seller_items[seller].append(item)
                
            for item in cart_items:
                item.delete()
                
            # Send notifications to sellers
            for seller, items in seller_items.items():
                message = f"You have new orders for the following products:\n"
                for item in items:
                    message += f"- {item.product.name}: {item.quantity} units\n"
                
                Notification.objects.create(
                    account=seller,
                    title='You have a new order',
                    content='Order #' + str(order.id),
                    ref='/seller/orders'
                )
            
            return redirect('/customer/order-complete/' + str(order.id))
        else:
            for error in errors:
                messages.error(request, error)
                
            return redirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponse('Invalid request')

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer'])     
def orderComplete(request, order_id):

    context = {
        'order_id' : order_id
    }

    return render(request, 'customer/order_complete.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer'])
def wishlist(request):
    
    if request.method == 'POST':
        account = Account.objects.get(email=request.user.email)
        
        search = request.POST.get('search')
        
        if search:
            wishlists = Wishlist.objects.filter(account=account, product__name__icontains=search)
        else:
            wishlists = Wishlist.objects.filter(account=account)

    else:
        account = Account.objects.get(email=request.user.email)
        
        wishlists = Wishlist.objects.filter(account=account)
            
    context = {
        'wishlists'  : wishlists,
        'page_title' : 'Wishlist',
        'referrer'   : '/customer/dashboard'
    }
    
    return render(request, 'customer/wishlist.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer'])
def addresses(request):
    
    account = Account.objects.get(email=request.user.email)
    
    addresses = Address.objects.filter(account=account)
    
    context = {
        'addresses'  : addresses,
        'page_title' : 'Address',
        'countries'  : countries,
        'referrer'   : '/customer/dashboard'
    }
    
    return render(request, 'customer/address.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer'])
def orders(request):
    
    account = Account.objects.get(email=request.user.email)
    
    orders  = Order.objects.filter(customer=account)
    
    context = {
        'orders'     : orders,
        'page_title' : 'Orders',
        'referrer'   : '/customer/dashboard'
    }
    
    return render(request, 'customer/orders.html', context)

@login_required(login_url='/auth/login')
@allowed_account(allowed_roles=['customer'])
def orderDetails(request, order_id):
    
    account = Account.objects.get(email=request.user.email)
    
    order = Order.objects.get(id=order_id)
    
    if order.customer == account:
        
        order_items = OrderItem.objects.filter(order=order)
    
        total = 0
        
        for order_item in order_items:
            total = total + order_item.price * order_item.quantity
        
        context = {
            'order'                 : order,
            'page_title'            : 'Order Details',
            'order_items'           : order_items,
            'total'                 : total,
            'referrer'              : '/customer/orders'
        }
        
        return render(request, 'customer/order_details.html', context)
    else:
        return redirect('unauthorized')
    
def deleteOrderItem(request, item_id):
    
    account = Account.objects.get(email=request.user.email)
    
    order_item = OrderItem.objects.get(id=item_id)
    
    if order_item.order.customer == account:
        order_item.delete()
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')
    
def cancelOrder(request, order_id):
    
    account = Account.objects.get(email=request.user.email)
    
    order = Order.objects.get(id=order_id)
    
    if order.customer == account:
        order.delete()
        
        return redirect('/customer/orders')
    else:
        return redirect('unauthorized')