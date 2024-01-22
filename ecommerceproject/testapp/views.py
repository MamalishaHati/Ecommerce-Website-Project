import queue
from django.shortcuts import render , redirect
from django.http import HttpResponse 
from django.http import JsonResponse
#from django.db.models import Count
from django.views import View
from testapp.models import Product ,Customer , Cart , Payment , OrderPlaced , Wishlist
from testapp.forms import CustomerRegistrationForm , CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
import razorpay
from django.conf import settings


def home_view(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'testapp/home.html',locals())

def about_view(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'testapp/about.html',locals())


def contact_view(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'testapp/contact.html',locals())



class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,'testapp/category.html',locals())

class CategoryTitle(View):
    def get(self,request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,'testapp/category.html',locals())


class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))

        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'testapp/productdetail.html',locals())

 

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request , 'testapp/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request , 'Congratulations! User Registration Successfully')
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request , 'testapp/customerregistration.html',locals())
    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request, 'testapp/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobilenumber = form.cleaned_data['mobilenumber']
            zipcode = form.cleaned_data['zipcode']
            #address = form.cleaned_data['address']

            reg = Customer(user=user,
                           name=name,
                           locality=locality,
                           city=city,
                           mobilenumber=mobilenumber,
                           zipcode=zipcode,
                           )
            reg.save()

            messages.success(request,'Congratulations ! profile save succesdsfulll')
        else:
            messages.warning(request,'Invalid Input data !')
        return render(request, 'testapp/profile.html',locals())
    

def address(request):
    address = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'testapp/address.html',locals())


class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'testapp/updateaddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.user = request.user
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobilenumber = form.cleaned_data['mobilenumber']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,'Congratulations ! profile Update Succesdsfulll')
        else:
            messages.warning(request,'Invalid Input data !')
        return redirect('address')
    

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/showcart')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount =0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 30
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request , 'testapp/addtocart.html',locals())


class checkout_cart(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount+ 30

        return render(request,'testapp/checkout.html',locals())

        #due to some razorside problem i'm gettings error that's why i'm commenting this
        '''
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {
            'amount':razoramount,
            'currency ':'INR',
            'receipt':'order_rcptid_13'
        }
        payment_response = client.order.create(data=data)
        print(payment_response)

        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        #return render(request,'testapp/checkout.html',locals())

def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    # return redirect("orders")
    customer = Customer.objects.grt(id=cust_id)
    payment = Payment.objrcts.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,
                    customer=customer,
                    product=c.product,
                    quantity=c.quantity,
                    payment=payment).save()
        c.delete()

    return redirect('orders')
    '''

"""def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request,'testapp/orders.html',locals())"""



def plus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity +=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0 
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value 
        totalamount = amount + 40
        #print(prod_id)
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

def minus_cart(request):
   if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity -=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0 
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value 
        totalamount = amount + 40
        #print(prod_id)
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0 
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value 
        totalamount = amount + 40
        #print(prod_id)
        data = {
            #'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user,product=product).save()
        data={
        'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)
        

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user,product=product).delete()
        data={
        'message': 'Wishlist Remove Successfully',
        }
        return JsonResponse(data)
        

def search_view(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains = query))
    return render(request,'testapp/search.html',locals())
