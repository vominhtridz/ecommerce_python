from myapp.models import UserProfile
from django.shortcuts import get_object_or_404
from myapp.models import Product
from myapp.models import Cart
from myapp.models import Notification
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def filter_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.filter(**kwargs)
    except classmodel.DoesNotExist:
        return None
def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
def currentUser_context(request):
    current_user = request.user if request.user.is_authenticated else None
    profile = None
    if current_user:
        profile = get_or_none(UserProfile, id=current_user.id)
        if profile is None:
            profile = UserProfile.objects.create(id=current_user.id)

    return {'current_user': current_user, 'Profile': profile}
       

def NotificationContext(request):
    current_time = timezone.now()
    current_user = request.user if request.user.is_authenticated else None
    user_notifications = None
    if current_user:
       user_notifications = filter_or_none(Notification, user_id = current_user.id)
    # Iterate over notifications to calculate time differences, assuming you have a timestamp field named 'created_at'
    
    # Print user_notifications for debugging purposes
    
    return {'Notifications': user_notifications}
def Product_context(request):
    Shoppings = Cart.objects.all()
    products = Product.objects.all()
    return {'products':products,'Shoppings':Shoppings}

    