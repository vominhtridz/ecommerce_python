from django.contrib import admin
from myapp.models import Image
from myapp.models import Comment
from myapp.models import UserProfile
from myapp.models import Notification
from myapp.models import CommentChild
from myapp.models import Product
from myapp.models import Cart
from myapp.models import Payment
from django.core.exceptions import FieldDoesNotExist


# Register your models here.

admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(Product)
admin.site.register(CommentChild)
admin.site.register(Cart)
admin.site.register(Payment)