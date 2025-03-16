from django.urls import path
from .views import oxapay_callback

urlpatterns = [
    path("callback/", oxapay_callback, name="oxapay_callback"),
]
