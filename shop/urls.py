from django.urls import path
from .views import (
    catalog, add_to_cart, view_cart, checkout, register, account,
    admin_auto_login, remove_from_cart, pay_order, add_product
)
from .views import edit_product as add_product
from django.conf import settings
from . import views


if settings.DEBUG:
   urlpatterns = [
        path('', views.index, name='index'),
    ]
urlpatterns = [
    path('', catalog, name='catalog'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('dashboard/add_product/', views.add_product, name='dashboard_add_product'),
    path('dashboard/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    # path('add_product/', views.add_or_edit_product, name='add_product'),
    # path('edit_product/<int:product_id>/', views.add_or_edit_product, name='edit_product'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),  
    path('checkout/', checkout, name='checkout'),
    path('register/', register, name='register'),
    path('account/', account, name='account'),
    path('admin_auto_login/', admin_auto_login, name='admin_auto_login'),
    path('dashboard/add_product/', add_product, name='add_product'),
    # path('pay/<int:order_id>/', views.pay_order, name='pay_order'),
    # path('pay/', pay_order, name='pay_order'),
]
