from django.contrib import admin
from testapp.models import Product , Customer , Cart , Payment , OrderPlaced ,Wishlist



class ProductModelAdmin(admin.ModelAdmin):
    list_display =['id','title','discounted_price','category','product_image'] 
admin.site.register(Product,ProductModelAdmin)


class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id','user','name','locality','city','mobilenumber','zipcode'] 
admin.site.register(Customer,CustomerModelAdmin)


class CartModelsAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']
admin.site.register(Cart,CartModelsAdmin)


class PaymentModelsAdmin(admin.ModelAdmin):
    list_display = ['id','user','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']
admin.site.register(Payment,PaymentModelsAdmin)


class OrderplacedModelsAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']
admin.site.register(OrderPlaced,OrderplacedModelsAdmin)

class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product',]
admin.site.register(Wishlist,WishlistModelAdmin)
