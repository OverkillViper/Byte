from django.shortcuts import render, redirect
from product.models   import *
from customer.models  import Cart
from seller.models    import Store
from django.db.models import Count, Subquery, OuterRef, Sum, Q

# Create your views here.
def home(request):
    
    new_products    = Product.objects.filter(published=True).order_by('-created_at')[:6]

    if Sell.objects.all().count() > 0:
        sell_quantity_subquery = Sell.objects.filter(orderItem__product=OuterRef('pk')).values('orderItem__product').annotate(total_quantity=Sum('quantity')).values('total_quantity')
    
        popular_products = Product.objects.filter(published=True).annotate(total_sales=Subquery(sell_quantity_subquery)).order_by('-total_sales')[:6]
    
    else:
        popular_products = None

    # Top Stores
    top_store_query = Sell.objects.filter(orderItem__product__store=OuterRef('pk')).values('orderItem__product__store').annotate(total_quantity=Sum('quantity')).values('total_quantity')

    top_stores = Store.objects.all().annotate(total_sales=Subquery(top_store_query)).order_by('-total_sales')[:6]

    top_stores_with_total_sale = []
    
    for store in top_stores:
        total_sale = Sell.objects.filter(orderItem__product__store=store).aggregate(total_quantity=Sum('quantity'))

        top_stores_with_total_sale.append({
            'store'      : store,
            'total_sale' : total_sale
        })

    context = {
        'new_products'      : new_products,
        'popular_products'  : popular_products,
        'top_stores'        : top_stores_with_total_sale,
    }
    
    return render(request, 'frontend/home.html', context)

def search(request):
    
    query = request.GET.get('q', '')  # Get the search query from the request

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query) |
            Q(store__name__icontains=query)
        )
        
        context = {
            'products' : products
        }
        
        return render(request, 'frontend/search_result.html', context)
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def stores(request):
    
    stores = Store.objects.all()
    
    top_stores_with_total_sale = []
    
    for store in stores:
        total_sale = Sell.objects.filter(orderItem__product__store=store).aggregate(total_quantity=Sum('quantity'))

        top_stores_with_total_sale.append({
            'store'      : store,
            'total_sale' : total_sale
        })
    
    context = {
        'stores' : top_stores_with_total_sale
    }
    
    return render(request, 'frontend/stores.html', context)

def storeDetails(request, store_id):
    
    store = Store.objects.get(id=store_id)
    
    products = Product.objects.filter(store=store).order_by('-created_at')
    
    context = {
        'products' : products,
        'store'    : store,
    }
    
    return render(request, 'frontend/store_details.html', context)

def products(request):
    
    filter = request.GET.get('filter')
    
    if filter == 'popular':
        if Sell.objects.all().count() > 0:
            sell_quantity_subquery = Sell.objects.filter(orderItem__product=OuterRef('pk')).values('orderItem__product').annotate(total_quantity=Sum('quantity')).values('total_quantity')
    
            products = Product.objects.filter(published=True).annotate(total_sales=Subquery(sell_quantity_subquery)).order_by('-total_sales')
        
        else:
            products = None
    elif filter == 'newest':
        products = Product.objects.filter(published=True).order_by('-created_at')
    else:
        products = Product.objects.filter(published=True)
        
    context = {
        'products' : products,
    }
    
    return render(request, 'frontend/products.html', context)

def categories(request):
    
    categories = Category.objects.filter(parent__isnull=False).exclude(
        id__in=Category.objects.filter(parent__isnull=False).values('parent_id')
    )
    
    context = {
        'categories' : categories,
    }
    
    return render(request, 'frontend/categories.html', context)

def category(request, category_id):
    
    category = Category.objects.get(id=category_id)
    
    product_categories = ProductCategory.objects.filter(category=category)
    
    context = {
        'products_categories' : product_categories,
        'category' : category,
    }
    
    return render(request, 'frontend/category.html', context)
