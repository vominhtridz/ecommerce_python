from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django_router import router
urlpatterns = [
    path('', views.home, name='home'),
    path('product_detail/<int:product_id>/', views.InforProduct, name='inforProduct'),
    path('cart/<int:user_id>/', views.CartPage, name='cart'),
    path('remove/<int:product_id>/', views.RemoveItemCart, name='cart'),
    path('addcart/<int:product_id>/', views.handleAddCart, name='cart'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/register/', views.register, name='register'),
    path('payment/<int:user_id>/', views.payment, name='payment'),
    path('profile/<int:user_id>/infor', views.Profile, name='profile'),
    path('profile/<int:user_id>/changepassword', views.changepassword, name='profile'),
    path('profile/<int:user_id>/notification', views.notification, name='profile'),
    path('profile/<int:user_id>/options', views.options, name='profile'),
    path('favorite/<int:user_id>/<int:product_id>/', views.handle_like, name='handle_like'),
    path('favorite_child/<int:user_id>/<int:product_id>/', views.handleLike_child, name='handle_like'),
    path('logout/', views.user_logout, name='logout'),
    path('comment_child/<int:product_id>/<int:comment_id>/', views.Handle_CommentChild, name='comment_child'),
    path('comment_tag/<int:product_id>/<int:comment_id>/<int:user_id>/<str:comment_tag>/', views.Handle_CommentTag, name='comment_tag'),
    re_path(r'^search/(?P<search_value>.+)/$', views.SearchPage, name='SearchPage'),
    path('comment/<int:product_id>/', views.Handle_Comment, name='comment'),
    path('payment', views.payment, name='payment'),
    path('payment_ipn', views.payment_ipn, name='payment_ipn'),
    path('payment_return', views.payment_return, name='payment_return'),
    path('query', views.query, name='query'),
    path('refund', views.refund, name='refund'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)