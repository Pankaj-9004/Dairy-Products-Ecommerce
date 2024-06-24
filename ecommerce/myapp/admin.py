from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced

# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'composition', 'prodapp', 'category', 'product_image']
    
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'name', 'locality', 'city', 'mobile', 'state', 'zipcode', 'image']
    
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']
    

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'order_date', 'status', 'payment']