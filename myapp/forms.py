from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myapp.models import UserProfile
from myapp.models import Comment
from myapp.models import CommentChild
class SignupForm(UserCreationForm):
    username = forms.CharField()
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']  # Specify the fields from User model
        

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'formInput', 'placeholder': 'Nhập username...'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'formInput', 'placeholder': 'Nhập mật khẩu...'})
    )
    
#--------------------------------------USER PROFILE FORM---------------------
class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'outline-blue-300 px-2 py-1.5 border border-gray-400 text-sm rounded-sm w-full', 'placeholder': 'Nhập email...'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'outline-blue-300 px-2 py-1.5 border border-gray-400 text-sm rounded-sm w-full', 'placeholder': 'Nhập địa chỉ...'}))
    day = forms.IntegerField(widget=forms.Select(attrs={'class': 'day border border-gray-400 rounded-sm px-3 py-1 mx-1'}))
    month = forms.IntegerField(widget=forms.Select(attrs={'class': 'month border border-gray-400 rounded-sm px-3 py-1 mx-1'}))
    year = forms.IntegerField(widget=forms.Select(attrs={'class': 'year border border-gray-400 rounded-sm px-3 py-1 mx-1'}))
    defaultName = forms.CharField(widget=forms.TextInput(attrs={'class': 'outline-blue-300 px-2 py-1.5 border border-gray-400 text-sm rounded-sm w-full', 'placeholder': 'Nhập tên...'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'px-2 py-1.5  text-sm rounded-sm w-full', 'placeholder': 'Nhập ...'}))
    gender = forms.CharField(widget=forms.Select(attrs={'class': 'border border-gray-500 text-sm px-4 py-1.5'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'outline-blue-300 px-2 py-1.5 border border-gray-400 text-sm rounded-sm w-full', 'placeholder': 'Nhập số điện thoại...'}))
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'day', 'month', 'year', 'defaultName', 'email', 'image', 'gender']
        
#--------------------------------------USER COMMENT FORM---------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']
        widgets = {
            'comment_content': forms.TextInput(attrs={'class': 'px-4 py-2 rounded-sm outline-gray-400 border border-gray-500 ml-3 mr-6 text-sm w-full', 'placeholder': 'Nhập nội dung bình luận'}),
        }
        
# -------------------------------------  COMMENT CHILD FORM ---------------------------------   
class CommentChildForm(forms.ModelForm):
    class Meta:
        model = CommentChild
        fields = ['comment_content']
        widgets = {
            'comment_content': forms.TextInput(attrs={'class': 'px-2 py-1  text-[13px] rounded-sm outline-gray-400 border border-gray-500 ml-3 mr-6 text-sm w-full', 'placeholder': 'Nhập nội dung bình luận....','id': 'CMT_child'}),
        }
        
class PaymentForm(forms.Form):

    order_id = forms.CharField(max_length=250)
    order_type = forms.CharField(max_length=20)
    amount = forms.IntegerField()
    order_desc = forms.CharField(max_length=100)
    bank_code = forms.CharField(max_length=20, required=False)
    language = forms.CharField(max_length=2)