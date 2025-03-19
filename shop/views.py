from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib.auth import login, get_user_model
from django.http import HttpResponse
from django.conf import settings
from .models import Product, Order, OrderItem, Category, CartItem
from .forms import RegisterForm, ProductForm
import stripe


# Настроим Stripe
# stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    return render(request, 'index.html')
    
def catalog(request):
    categories = Category.objects.all()
    q = request.GET.get('q', '')
    c = request.GET.get('cat', '')
    products = Product.objects.filter(available=True)
    if c:
        products = products.filter(category_id=c)
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    return render(request, 'catalog.html', {'categories': categories, 'products': products})

@login_required 
# проверяет, что пользователь вошел в систему. 
# Если он не авторизован, то он будет перенаправлен на страницу входа.
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('catalog')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        items.append({'product': product, 'quantity': qty})
        total += product.price * qty
    return render(request, 'cart.html', {'items': items, 'total': total})

def remove_from_cart(request, product_id):
    # """Удаляет товар из корзины"""
    item = get_object_or_404(CartItem, product__id=product_id, user=request.user)
    item.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('catalog')
        shipping = request.POST.get('shipping', 'pickup')
        total = 0
        for pid, qty in cart.items():
            product = Product.objects.get(id=pid)
            total += product.price * qty
        order = Order.objects.create(user=request.user, total_price=total, shipping_method=shipping)
        for pid, qty in cart.items():
            product = Product.objects.get(id=pid)
            OrderItem.objects.create(order=order, product=product, quantity=qty)
        request.session['cart'] = {}
        return render(request, 'order_confirmation.html', {'order': order})
    return redirect('view_cart')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalog')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def account(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'account.html', {'orders': orders})

def admin_auto_login(request):
    telegram_id_str = request.GET.get('telegram_id')
    token = request.GET.get('token')
    if telegram_id_str and token:
        try:
            telegram_id = int(telegram_id_str)
        except ValueError:
            return HttpResponse("Некорректный Telegram ID")
        if token != settings.ADMIN_AUTO_LOGIN_TOKEN:
            return HttpResponse("Неверный токен")
        if telegram_id in settings.TELEGRAM_ADMIN_IDS:
            User = get_user_model()
            username = f"tg_{telegram_id}"
            user, created = User.objects.get_or_create(username=username)
            user.is_staff = True  # выдаём права администратора
            user.save()
            login(request, user)
            return redirect('catalog')
        else:
            return HttpResponse("Нет прав администратора")
    return HttpResponse("Telegram ID или токен не указаны")

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

@admin_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

from django.shortcuts import render

@admin_required
def pay_order(request):
    # Ваш код обработки платежа
    return render(request, 'shop/pay_order.html')



