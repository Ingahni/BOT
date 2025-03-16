from django.urls import path
from .views import (
    catalog, add_to_cart, view_cart, checkout, register, account,
    admin_auto_login, add_product
)


urlpatterns = [
    path('', catalog, name='catalog'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
    path('register/', register, name='register'),
    path('account/', account, name='account'),
    path('admin_auto_login/', admin_auto_login, name='admin_auto_login'),
    path('dashboard/add_product/', add_product, name='add_product'),
    

]
