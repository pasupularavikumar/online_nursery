
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest 
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import razorpay
from .models import Product, placedOrder
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

 
 
 
 
 
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


from accounts.models import Product, cartObject, placedOrder

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,"about.html")


def  shop(request):
    return render(request,"shop.html")

def checkout(request):
    prdList = []
    totalPrice = 500
    print(list(cartObject.objects.filter(user=request.user)))
    for p in list(cartObject.objects.filter(user=request.user)):
        prdList.append({
            "name":p.products.name,
            "quantity":p.quantity,
            "price":p.products.price,
            "total":p.products.price * p.quantity
        })
        totalPrice += p.products.price * p.quantity
    razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    currency = 'INR'
    amount = totalPrice  # Rs. 200
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    # user = User.objects.filter()
    context['user_name'] = request.user
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['products'] = prdList
    context['subtotal'] = totalPrice - 50
    context['totalPrice'] = totalPrice 
    context['shippingCharge'] = 50
    context['is_payment_gateway']= False
    context['email'] = ''
    context['address'] = ''
    context['phone'] = ''

    if request.method == 'POST':
        name=request.POST["name"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        address=request.POST["address"]
        context['email'] = email
        context['address'] = address
        context['phone'] = phone
        placedOrdernew = placedOrder.objects.create(name=name, email=email, phone=phone, address=address, user=request.user)
        placedOrdernew.save()
        context['is_payment_gateway'] = True
    return render(request,"checkout.html", context)

def news(request):
    return render(request,"news.html")


def loginPage(request):
    if(request.method=="POST"):
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Username or password incorrect") 
            return redirect("/")     
        


def signUp(request):
    if(request.method=="POST"):
        username=request.POST["username"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        email=request.POST["email"]
        user=User.objects.create_user(username=username,password=password1,email=email)
        user=user.save()
        return redirect("/")
    return HttpResponse("SSS")

def logoutUser(request):
    logout(request)
    return redirect("/")


def shop(request):
    flowers=Product.objects.all()
    return render(request,'shop.html',{'flowers':flowers})

def singleProduct(request,pk):
    product=Product.objects.get(id=pk)
    relatedproducts=product.relatedproduct.all()
    return render(request,'single-product.html',{'product':product,'relatedproducts':relatedproducts})
    

def cart(request):
    if request.method=="POST":
        id=request.POST["id"]
        quantity=request.POST["quantity"]
        carts=cartObject.objects.create(products=Product.objects.get(id=id),user=request.user,quantity=quantity)
        carts.save()
        return redirect("/")

def allCart(request):
    carts=cartObject.objects.filter(user=request.user)
    total=0
    for cart in carts:
        total+=cart.products.price*cart.quantity

    return render(request,'cart.html',{'carts':carts, 'grandtotal':total+50, 'Subtotal':total})

def removeCart(request,id):
    cartObject.objects.filter(products=Product.objects.get(id=id),user=request.user).delete()
    return redirect("/cart")


 
 
# authorize razorpay client with API Keys.

 
def paymentcheckout(request):
    razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'payment.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

def seller_login(request):
    if request.user.is_superuser:
        return redirect('seller_dashboard')
    else:
        if(request.method=="POST"):
            username=request.POST["username"]
            password=request.POST["password"]
            user=authenticate(request,username=username,password=password)
            if user is not None and user.is_staff:
                login(request,user)
                return redirect('seller_dashboard')
            else:
                return render(request,'seller-login.html',{"error":'Username or password is incorrect or not exists !'})
        return render(request,'seller-login.html')

def seller_logout(request):
    logout(request)
    return redirect("seller_login")

def seller_dashboard(request):
    if request.user.is_staff:
        total_user = len(User.objects.all())
        total_products = len(Product.objects.all())
        total_orders = len(placedOrder.objects.all())
        return render(request,'seller-dashboard.html',{'total_user':total_user,'total_products':total_products,'total_orders':total_orders})
    return redirect('seller_login')

def seller_users(request):
    if request.user.is_staff:
        return render(request,'seller-users.html',{'users':list(User.objects.all())})
    return redirect('seller_login')

def seller_products(request):
    if request.user.is_staff:
        return render(request,'seller-products.html',{'products':list(Product.objects.all())})
    return redirect('seller_login')

def seller_add_product(request):
    if request.user.is_staff:
        if request.method=='POST':
            name=request.POST["name"]
            price=request.POST["price"]
            categories=request.POST["categories"]
            description=request.POST["description"]
        return render(request,'seller-add-product.html')
    return redirect('seller_login')

def seller_orders(request):
    if request.user.is_staff:
        return render(request,'seller-orders.html')
    return redirect('seller_login')
    

