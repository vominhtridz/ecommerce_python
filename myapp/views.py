
from django.shortcuts import get_object_or_404, render, redirect,HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from myapp.forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from myapp.forms import SignupForm, LoginForm
from myapp.models import Image
from myapp.models import Comment
from myapp.models import CommentChild
from myapp.models import Product
from myapp.models import Cart
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from myapp.models import UserProfile
from myapp.models import Notification
from myapp.forms import CommentChildForm
from myapp.forms import CommentForm
from django.contrib.auth.hashers import check_password
from myapp.forms import UserProfileForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import pytz
from django.urls import reverse
# Create your views here.
def home(request):
    images = Image.objects.all()
    return render(request, 'home.html', {'images': images})
def InforProduct(request, product_id):
    product = Product.objects.get(id=product_id)
    class MyObject:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    my_object = MyObject(**product.information)
    formatted_number = f"{product.price:,}"
    current_user = request.user if request.user.is_authenticated else None
    Post_Comment =Comment.objects.filter(product_id=product_id) 
    comment_temp = CommentForm()
    #child
    Post_CommentChild =CommentChild.objects.filter(product_id=product_id)
    commentChild_temp = CommentChildForm()
    context = {'product': product,
               'product_price': formatted_number, 
               'information': my_object,
               'current_user':current_user, 
               'Post_CommentChild': Post_CommentChild, 
                'comment_temp':comment_temp,
                'Post_Comments':Post_Comment,
                'commentChild_temp':commentChild_temp}
    return render(request, 'inforProduct.html', context)

# ----------------------------------------HANDLE SEARCH PAGE  -------------------
def SearchPage(request, search_value):
    # Kiểm tra xem search_value có rỗng không
    PostsResult = Product.objects.filter(title=search_value)
    print('result', PostsResult)
    context = {'PostsResult': PostsResult, 'title': search_value}
    return render(request, 'SearchPage.html', context)
# --------------------------------------CART Page -------------------------
@login_required
def CartPage(request,user_id):
    Carts = Cart.objects.all()
    payment = sum(product.price * product.quality for product in Carts)
    # Format the payment amount with commas for better readability
    formatted_payment = f"{payment:,}"

    context = {
        'ShoppingCarts': Carts,
        'Payment': formatted_payment
    }
    return render(request, 'Cart.html', context)
def RemoveItemCart(request, product_id):
    current_user = request.user if request.user.is_authenticated else None
    if request.method == 'POST':
        url = f"/cart/{current_user.id}/"
        Cart.objects.get(product_id=product_id).delete()
        return redirect(url)
def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
@login_required
def handleAddCart(request, product_id):
    current_user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        existing_cart_item = get_or_none(Cart, product_id=product_id)
        if existing_cart_item:
            existing_cart_item.quality += 1
            existing_cart_item.save()
        else:
            Cart.objects.create(
                image=product.image,
                title=product.title,
                product_id=product_id,
                user_id=current_user.id if current_user else None,
                price=product.price,
                color=product.color,
            )
        return redirect('cart', user_id=current_user.id if current_user else None)
    else:
        return redirect('product', product_id=product_id)
    
        
#Like
def handle_like (request,user_id,product_id ):
    CMT = Comment.objects.get(id = user_id)
    if 'Like' in request.POST:
        CMT.like +=1
        redirect('comment', product_id)  
    elif "Dislike" in request.POST:
        CMT.like += 1
    
    CMT.save()
    return redirect('comment', product_id)
        

def handleLike_child (request, user_id,post_id):
    CMTChild = CommentChild.objects.get(user_id = user_id)
    if 'Like' in request.POST:
        CMTChild.like +=1
        return redirect('comment', post_id)
    elif "Dislike" in request.POST:
        CMTChild.like += 1
    CMTChild.save()    
    return redirect('comment', post_id)
# Change Password 
@login_required
def changepassword(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        if check_password(old_password, user.password):
            if old_password == new_password:
                messages.error(request, 'New password is the same as old password')
            else:
                # Set the new password and save the user
                user.set_password(new_password)
                user.save()           
                messages.success(request, 'Password changed successfully')
        else:
            messages.error(request, 'Old password is incorrect')
    return render(request, 'ChangePassword.html')
# Change Password 
@login_required
def notification(request,user_id):
    return render(request, 'notification.html')
    # Change Password 
@login_required
def options(request,user_id):
    return render(request, 'options.html')

@login_required
def Profile(request, user_id):

    current_user = request.user if request.user.is_authenticated else None
    DefaultProfile = None
    if current_user:
        try:
            DefaultProfile = UserProfile.objects.get(id=current_user.id)
        except ObjectDoesNotExist:
            DefaultProfile = UserProfile.objects.create(id=current_user.id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=DefaultProfile)
        # save image and username to Comment
        # check form valid
        if form.is_valid():
            FormDB = form.save(commit=False)
            FormDB.id = user_id
            form.save()
            messages.success(request, 'Lưu thông tin cá nhân thành công.')
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=DefaultProfile)     

    context = { 'current_user': current_user, 'form': form, 'DefaultProfile': DefaultProfile}
    return render(request, 'Profile.html', context)
      
      
  # Comment 
@login_required
  
def Handle_Comment(request, product_id):
    current_user = request.user if request.user.is_authenticated else None
    url = f"/product_detail/{product_id}/"
    if request.method == 'POST':
        profile = get_or_none(UserProfile,id=current_user.id)
        vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        LengthCMTChild = len(Comment.objects.filter(product_id=product_id))
        comment_temp = CommentForm(request.POST)
        if comment_temp.is_valid():
            comment_DB = comment_temp.save(commit=False)
            comment_DB.product_id = product_id
            comment_DB.user_id = current_user.id
            comment_DB.Commentid = LengthCMTChild
            comment_DB.comment_content = comment_temp.cleaned_data['comment_content']
            comment_DB.author = current_user
            if profile.image:
                comment_DB.image = profile.image
                comment_DB.username = profile.defaultName
            comment_DB.created_at = timezone.now().astimezone(vietnam_timezone)
            comment_DB.save()
        return redirect(url)
     
    else:   
        return redirect(url)
     

    
    
 # -------------------handle Comment child---------------------
 
def Handle_CommentChild(request, product_id,comment_id):

    
    current_user = request.user if request.user.is_authenticated else None
    profile = get_object_or_404(UserProfile, id = current_user.id)
    # Lấy bài viết theo id  
    comment_instant = Comment.objects.get(id = comment_id)
    comment_instant.reply_count += 1
    comment_instant.save(update_fields=['reply_count'])
    if request.method == 'POST':
        responder = request.POST.get('comment_author')
        comment_template = CommentChildForm(request.POST)
        if comment_template.is_valid():
            CommentChild_DB = comment_template.save(commit=False)
            CommentChild_DB.product_id = product_id
            CommentChild_DB.user_id = current_user.id
            CommentChild_DB.tag = ''
            CommentChild_DB.comment_content = comment_template.cleaned_data['comment_content']
            CommentChild_DB.author = current_user
            CommentChild_DB.commentChild_id = comment_id
            
            if profile.image:
                CommentChild_DB.image = profile.image
                CommentChild_DB.username = profile.defaultName
            CommentChild_DB.responder = responder
            CommentChild_DB.created_at  = timezone.now()
            if comment_id != current_user.id:
                Notification.objects.create(
                username = profile.defaultName,
                user_id = current_user.id,
                message=str(comment_template.cleaned_data['comment_content']), 
                created_at=timezone.now(),
                image=profile.image,
                to='product_detail/%s/' % product_id  
                )
            CommentChild_DB.save()  
    return redirect('comment', product_id) 


 # -------------------handle Comment tag---------------------

def Handle_CommentTag(request, product_id,comment_id,user_id,comment_tag):

    current_user = request.user if request.user.is_authenticated else None
    profile = get_object_or_404(UserProfile, id = current_user.id)
    comment = Comment.objects.get(id = comment_id)
    comment.reply_count +=1
    comment.save(update_fields=['reply_count'])
    if request.method == 'POST':
        responder = request.POST.get('comment_author')
        comment_template = CommentChildForm(request.POST)
        if comment_template.is_valid():
            CommentChild_DB = comment_template.save(commit=False)
            CommentChild_DB.product_id = product_id
            CommentChild_DB.user_id = current_user.id
            # Check to set user tag 
            if current_user.id == user_id:
                CommentChild_DB.tag = ''
            else:
                CommentChild_DB.tag = comment_tag
            CommentChild_DB.comment_content = comment_template.cleaned_data['comment_content']
            CommentChild_DB.author = current_user
            # handle Like
            
            if profile.image:
                CommentChild_DB.image = profile.image
                CommentChild_DB.username = profile.defaultName
            CommentChild_DB.commentChild_id = comment_id
            CommentChild_DB.responder = responder
            CommentChild_DB.created_at  = timezone.now()
            if comment_id != current_user.id:
                Notification.objects.create(
                username = profile.defaultName,
                user_id = current_user.id,
                message=str(comment_template.cleaned_data['comment_content']), 
                created_at=timezone.now(),
                image=profile.image,
                to='product_detail/%s/' % product_id  
                )
            CommentChild_DB.save()  
    return redirect('comment', product_id)      
      
      
      
def login(request):  
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  
                messages.success(request, 'Đăng nhập thành công')
                
                return redirect('home')
            else:
                messages.error(request, 'Có lỗi xảy ra')
                
                form.add_error(None, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'form': form, 'error_message': 'Username already exists.'})
            else:
                # Username is unique, save the form data
                form.save()
                messages.success(request, 'Đăng kí thành công')
                return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')
def payment(request,user_id):
    return render(request, 'payment.html')
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import random
import requests
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import unquote

from .forms import PaymentForm
from .vnpay import vnpay


def index(request):
    return render(request, "index.html", {"title": "Danh sách demo"})


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def payment(request):

    if request.method == 'POST':
        # Process input data and build url payment
        form = PaymentForm(request.POST)
        if form.is_valid():
            order_type = form.cleaned_data['order_type']
            order_id = form.cleaned_data['order_id']
            amount = form.cleaned_data['amount']
            order_desc = form.cleaned_data['order_desc']
            bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data['language']
            ipaddr = get_client_ip(request)
            # Build URL Payment
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
            vnp.requestData['vnp_Amount'] = amount * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type
            # Check language, default: vn
            if language and language != '':
                vnp.requestData['vnp_Locale'] = language
            else:
                vnp.requestData['vnp_Locale'] = 'vn'
                # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
            if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
            print(vnpay_payment_url)
            return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
    else:
        return render(request, "payment.html", {"title": "Thanh toán"})


def payment_ipn(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = True
            totalamount = True
            if totalamount:
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    # Return VNPAY: Merchant update success
                    result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    # Already Update
                    result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})
            else:
                # invalid amount
                result = JsonResponse({'RspCode': '04', 'Message': 'invalid amount'})
        else:
            # Invalid Signature
            result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

    return result


def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Thành công", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
            else:
                return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Lỗi", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
        else:
            return render(request, "payment_return.html",
                          {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                           "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                           "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"})
    else:
        return render(request, "payment_return.html", {"title": "Kết quả thanh toán", "result": ""})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

n = random.randint(10**11, 10**12 - 1)
n_str = str(n)
while len(n_str) < 12:
    n_str = '0' + n_str


def query(request):
    if request.method == 'GET':
        return render(request, "query.html", {"title": "Kiểm tra kết quả giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_Version = '2.1.0'

    vnp_RequestId = n_str
    vnp_Command = 'querydr'
    vnp_TxnRef = request.POST['order_id']
    vnp_OrderInfo = 'kiem tra gd'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode,
        vnp_TxnRef, vnp_TransactionDate, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "query.html", {"title": "Kiểm tra kết quả giao dịch", "response_json": response_json})

def refund(request):
    if request.method == 'GET':
        return render(request, "refund.html", {"title": "Hoàn tiền giao dịch"})

    url = settings.VNPAY_API_URL
    secret_key = settings.VNPAY_HASH_SECRET_KEY
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_RequestId = n_str
    vnp_Version = '2.1.0'
    vnp_Command = 'refund'
    vnp_TransactionType = request.POST['TransactionType']
    vnp_TxnRef = request.POST['order_id']
    vnp_Amount = request.POST['amount']
    vnp_OrderInfo = request.POST['order_desc']
    vnp_TransactionNo = '0'
    vnp_TransactionDate = request.POST['trans_date']
    vnp_CreateDate = datetime.now().strftime('%Y%m%d%H%M%S')
    vnp_CreateBy = 'user01'
    vnp_IpAddr = get_client_ip(request)

    hash_data = "|".join([
        vnp_RequestId, vnp_Version, vnp_Command, vnp_TmnCode, vnp_TransactionType, vnp_TxnRef,
        vnp_Amount, vnp_TransactionNo, vnp_TransactionDate, vnp_CreateBy, vnp_CreateDate,
        vnp_IpAddr, vnp_OrderInfo
    ])

    secure_hash = hmac.new(secret_key.encode(), hash_data.encode(), hashlib.sha512).hexdigest()

    data = {
        "vnp_RequestId": vnp_RequestId,
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Command": vnp_Command,
        "vnp_TxnRef": vnp_TxnRef,
        "vnp_Amount": vnp_Amount,
        "vnp_OrderInfo": vnp_OrderInfo,
        "vnp_TransactionDate": vnp_TransactionDate,
        "vnp_CreateDate": vnp_CreateDate,
        "vnp_IpAddr": vnp_IpAddr,
        "vnp_TransactionType": vnp_TransactionType,
        "vnp_TransactionNo": vnp_TransactionNo,
        "vnp_CreateBy": vnp_CreateBy,
        "vnp_Version": vnp_Version,
        "vnp_SecureHash": secure_hash
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = json.loads(response.text)
    else:
        response_json = {"error": f"Request failed with status code: {response.status_code}"}

    return render(request, "refund.html", {"title": "Kết quả hoàn tiền giao dịch", "response_json": response_json})