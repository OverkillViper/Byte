from django.db                  import models
from hashid_field               import HashidAutoField
from seller.models              import Store
from accounts.models            import Account, Address, Notification
from django.utils               import timezone
from datetime                   import datetime, timedelta
from django.db.models.functions import TruncDate
from django.db.models           import Count, Subquery, OuterRef, Sum

import os
import uuid

def product_image_path(instance, filename):
    ext         = filename.split('.')[-1]
    filename    = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/products', filename)

# Create your models here.
class Product(models.Model):
    
    id              = HashidAutoField(primary_key=True)
    name            = models.CharField(max_length=255)
    description     = models.TextField(default='')
    price           = models.IntegerField(default=0)
    discount        = models.IntegerField(default=0)
    in_stock        = models.BooleanField(default=False)
    published       = models.BooleanField(default=False)
    brand           = models.CharField(max_length=255)
    model           = models.CharField(max_length=255)
    warranty        = models.CharField(max_length=255)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    store           = models.ForeignKey(Store, on_delete=models.CASCADE)
    account         = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    def category(self):
        return ProductCategory.objects.get(product=self).category
    
    def first_gallery(self):
        return Gallery.objects.filter(product=self).order_by('display_order').first()
    
    def discounted_price(self):
        return self.price - (self.price * (self.discount / 100))
    
    def __str__(self):
        return self.name
    
    def rating(self):
        reviews = Review.objects.filter(orderItem__product=self)
        
        total_rating = 0
        total_review = reviews.count()
        
        if total_review > 0:
            for review in reviews:
                if review.rating is not None:
                    total_rating = total_rating + review.rating
            
            rating = total_rating / total_review
        else:
            rating = 0
        
        return str(rating) + ' (' + str(total_review) + ')'
    
    def itemSold(self):
        sells = Sell.objects.filter(orderItem__product=self)
        
        totalSold = 0
        
        for sell in sells:
            totalSold = totalSold + sell.quantity
            
        return totalSold
        
    
class Gallery(models.Model):
    
    id            = HashidAutoField(primary_key=True)
    product       = models.ForeignKey(Product, on_delete=models.CASCADE)
    image         = models.FileField(upload_to=product_image_path, max_length=None)
    display_order = models.IntegerField(null=True)
    
    def save(self, *args, **kwargs):
        if self.id is None:
            other_galleries = Gallery.objects.filter(product=self.product)
            if other_galleries.exists():
                max_display_order = other_galleries.aggregate(models.Max('display_order'))['display_order__max']
                self.display_order = max_display_order + 1
            else:
                self.display_order = 0
        super().save(*args, **kwargs)
    
    @staticmethod
    def renumber_display_order(product):
        galleries = Gallery.objects.filter(product=product).order_by('display_order')
        for index, gallery in enumerate(galleries):
            gallery.display_order = index
            gallery.save()
    
    def delete(self, *args, **kwargs):
        product = self.product
        # Ensure file deletion
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)
        Gallery.renumber_display_order(product)
    
    def swap_with(self, other_gallery):
        if other_gallery and self.product == other_gallery.product:
            self.display_order, other_gallery.display_order = other_gallery.display_order, self.display_order
            self.save()
            other_gallery.save()

    def move_up(self):
        previous_gallery = Gallery.objects.filter(
            product=self.product,
            display_order__lt=self.display_order
        ).order_by('-display_order').first()
        if previous_gallery:
            self.swap_with(previous_gallery)

    def move_down(self):
        next_gallery = Gallery.objects.filter(
            product=self.product,
            display_order__gt=self.display_order
        ).order_by('display_order').first()
        if next_gallery:
            self.swap_with(next_gallery)
    
    def __str__(self):
        return str(self.id)
    
class Category(models.Model):
    
    id            = HashidAutoField(primary_key=True)
    parent        = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name          = models.CharField(max_length=100)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class ProductCategory(models.Model):
    
    id            = HashidAutoField(primary_key=True)
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    product       = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at    = models.DateTimeField(auto_now_add=True)
    
    def delete(self, *args, **kwargs):
        product = Product.objects.get(id=self.product.id)
        product.delete()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return self.category.name
    
class ProductAttribute(models.Model):
    
    id          = HashidAutoField(primary_key=True)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    name        = models.CharField(max_length=255)
    value       = models.CharField(max_length=255, blank=True)
    parent      = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
   
    STATUS = (
        ('processing', 'processing' ),
        ('accepted',   'accepted'   ),
        ('shipped',    'shipped'    ),
        ('delivered',  'delivered'  ),
    )
    
    PAYMENT = (
        ('cashless', 'cashless' ),
        ('cod',      'cod'      ),
    )
    
    id           = HashidAutoField(primary_key=True)
    customer     = models.ForeignKey(Account, on_delete=models.CASCADE)
    status       = models.CharField(max_length=50, choices=STATUS, default='processing')
    address      = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment      = models.CharField(max_length=50, choices=PAYMENT, default='cashless')
    
    created_at   = models.DateTimeField(auto_now_add=True)
    approved_at  = models.DateTimeField(null=True)
    shipped_at   = models.DateTimeField(null=True)
    delivered_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Fetch the existing status from the database
            previous_order = Order.objects.get(pk=self.pk)
            previous_status = previous_order.status
            
            # Check if the status has changed
            if previous_status != self.status:
                now = timezone.now()
                
                # Update timestamps based on the new status
                if self.status == 'accepted':
                    self.approved_at = now
                    self.shipped_at = None
                    self.delivered_at = None
                elif self.status == 'shipped':
                    self.approved_at = now if self.approved_at is None else self.approved_at
                    self.shipped_at = now
                    self.delivered_at = None
                elif self.status == 'delivered':
                    self.approved_at = now if self.approved_at is None else self.approved_at
                    self.shipped_at = now if self.shipped_at is None else self.shipped_at
                    self.delivered_at = now
                else:  # 'processing'
                    self.approved_at = None
                    self.shipped_at = None
                    self.delivered_at = None
        
        super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    
    STATUS = (
        ('processing', 'processing'    ),
        ('accepted',   'accepted'   ),
        ('shipped',    'shipped'    ),
        ('delivered',  'delivered'  ),
    )
    
    id           = HashidAutoField(primary_key=True)
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)
    status       = models.CharField(max_length=50, choices=STATUS, default='processing')
    order        = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity     = models.IntegerField(default=1)
    price        = models.IntegerField(default=0)
    
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        status_levels = ['processing', 'accepted', 'shipped', 'delivered']
        
        # Get all OrderItems for the same Order
        order_items = OrderItem.objects.filter(order=self.order)
        
        # Check if all OrderItems have the same status
        min_status_level = min(order_items.values_list('status', flat=True), key=status_levels.index)

        prev_order_status = self.order.status
        
        self.order.status = min_status_level
        self.order.save()
        
        if self.order.status != prev_order_status:
            # Send notification to customer
            notification = Notification(
                account = self.order.customer,
                title   = 'Your order has been ' + min_status_level,
                content = 'Order #' + str(self.order.id),
                ref     = '/customer/order/details/' + str(self.order.id),
            )
            
            notification.save()
            
            if self.order.status == 'delivered':
                for order_item in order_items:
                    sell = Sell(
                        customer     = order_item.order.customer,
                        seller       = order_item.product.account,
                        price        = order_item.price,
                        quantity     = order_item.quantity,
                        orderItem    = order_item
                    )
                
                    sell.save()

                for order_item in order_items:                    
                    review = Review(account=order_item.order.customer, orderItem=order_item)
                    review.save()
                    
    def getReview(self):
        review = Review.objects.get(orderItem=self)
        
        return review
                    
class Sell(models.Model):
    
    id           = HashidAutoField(primary_key=True)
    customer     = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='customer')
    seller       = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='seller')
    price        = models.IntegerField(default=0)
    quantity     = models.IntegerField(default=0)
    orderItem    = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='orderItem')
    
    created_at   = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id
    
    def get_days_in_current_month():
        now                     = timezone.now()
        first_day_of_month      = now.replace(day=1)
        next_month              = first_day_of_month + timedelta(days=32)
        first_day_of_next_month = next_month.replace(day=1)
        days_in_month           = (first_day_of_next_month - first_day_of_month).days
        
        return [(first_day_of_month + timedelta(days=i)).date() for i in range(days_in_month)]

    def get_current_month_sell(account):
        now = timezone.now()
        first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = first_day_of_month + timedelta(days=32)
        first_day_of_next_month = next_month.replace(day=1)
        
        if account.role == 'admin':
            current_month_sell = Sell.objects.filter(
                created_at__gte=first_day_of_month,
                created_at__lt=first_day_of_next_month
            ).annotate(day=TruncDate('created_at')).values('day').annotate(total_quantity=Sum('quantity')).order_by('day')
        elif account.role == 'seller':
            current_month_sell = Sell.objects.filter(
                orderItem__product__account=account,
                created_at__gte=first_day_of_month,
                created_at__lt=first_day_of_next_month
            ).annotate(day=TruncDate('created_at')).values('day').annotate(total_quantity=Sum('quantity')).order_by('day') 
        elif account.role == 'customer':
            current_month_sell = Sell.objects.filter(
                orderItem__order__customer=account,
                created_at__gte=first_day_of_month,
                created_at__lt=first_day_of_next_month
            ).annotate(day=TruncDate('created_at')).values('day').annotate(total_quantity=Sum('quantity')).order_by('day')
        
        counts_by_day = {item['day']: item['total_quantity'] for item in current_month_sell}
        days_in_month = Sell.get_days_in_current_month()
        
        data = [{'day': day, 'count': counts_by_day.get(day, 0)} for day in days_in_month]
        
        return data
    
class Review(models.Model):
    
    id           = HashidAutoField(primary_key=True)
    account      = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating       = models.IntegerField(null=True, blank=True)
    orderItem    = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True)
    
    created_at   = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.orderItem.product.name