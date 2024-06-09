from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images')
    
class Cart(models.Model):
    colorChoices = (
        ('Xám','Xám'),
        ('Xanh','Xanh'),
        ('Đen','Đen')
    )
    title = models.CharField(default='',max_length=150)
    image = models.ImageField(upload_to='product/images')    
    product_id = models.IntegerField(default=1)
    user_id = models.IntegerField(default= 1)
    price = models.IntegerField(default=1)
    quality= models.IntegerField(default=1)
    color =  models.CharField(default='', choices=colorChoices,max_length=20)
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('Thành công','Thành công'),
        ('Thất bại','Thất bại'),
    )
    order_id = models.IntegerField(default=1)
    amount = models.IntegerField(default=1)
    pay = models.ImageField(default=1)
    order_desc = models.CharField(default='chuyển tiền',max_length=150)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments') 
class Product(models.Model):
    colorChoices = (
        ('Xám','Xám'),
        ('Xanh','Xanh'),
        ('Đen','Đen')
    )
    AddressChoices = (
    ('Đà nẵng', 'Đà nẵng'),
    ('Hà nội', 'Hà nội'),
    ('TP HCM', 'TP HCM'),
    ('Quảng ngãi', 'Quảng ngãi'))

    image = models.ImageField(upload_to='product/images')    
    title = models.CharField(default='',max_length=150)
    price = models.IntegerField(default=1)
    color =  models.CharField(default='', choices=colorChoices,max_length=20)
    address =  models.CharField(default='', choices=AddressChoices,max_length=20)
    stars = models.IntegerField(default=1)
    evaluateCount = models.IntegerField(default=0)
    information = models.JSONField(null= True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.title
class Notification(models.Model):
    username = models.CharField(default='user', max_length=100)
    user_id = models.IntegerField(default=1)
    message = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(default=timezone.now)
    to = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to='profiles/images',default='/static/images/user-icon.png')
    

class UserProfile(models.Model):
    choices_gender= (
        ('Nam','Nam'),
        ('Nữ','Nữ'),
        ('Khác','Khác')
    )
    choices_day = [(i, i) for i in range(1, 32)]  # Days from 1 to 31
    choices_month = [(i, i) for i in range(1, 13)]  # Months from 1 to 12
    day = models.IntegerField( choices= choices_day,default=1)
    month = models.IntegerField( choices= choices_month,default=1)
    year = models.IntegerField(default=2010)
    address = models.CharField(max_length=200, blank=True, null=True,default='')
    phone_number = models.CharField(blank=True,max_length=11, null=True,default= '')
    defaultName = models.CharField(blank=True,max_length=30,default= 'User')
    image = models.ImageField(upload_to='profiles/images',default='/static/images/user-icon.png')
    email = models.EmailField(blank= True, default='example@gmail.com')
    gender = models.CharField(default='Nam', choices=choices_gender,max_length=20)
    def __str__(self):
        return self.defaultName   
    
# ---------------------COMMENT FATER -------------------   
class Comment(models.Model):
    user_id = models.IntegerField(default= 1)
    Commentid = models.IntegerField(default=1)
    product_id = models.IntegerField(default=1)
    comment_content = models.TextField(default='')
    created_at = models.DateTimeField(default=timezone.now)
    reply_count = models.IntegerField(default= 0,blank= True)
    like = models.IntegerField(default = 0)
    dislike = models.IntegerField(default = 0)
    username= models.CharField(default= 'user',blank=True,max_length=50)
    image = models.ImageField(upload_to='comment/images',default='static/images/user-icon.png')

# --------------------  COMMENT CHILD -------------------   

class CommentChild(models.Model):
    tag = models.CharField(max_length=150,blank= True)
    user_id = models.IntegerField(default= 1)
    username= models.CharField(default= 'user',blank=True,max_length=50)
    image = models.ImageField(upload_to='comment/images',default='static/images/user-icon.png')
    product_id = models.IntegerField(default=1)
    commentChild_id = models.IntegerField(default=1)
    responder = models.CharField(max_length=150)
    comment_content = models.TextField(default='')
    created_at = models.DateTimeField(default=timezone.now)
    like = models.IntegerField(default = 0)
    dislike = models.IntegerField(default = 0)
    
    
