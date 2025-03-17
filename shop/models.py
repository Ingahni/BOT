from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидайте доставку'),
        ('confirmed', 'Подтверждён'),
        ('canceled', 'Отменён'),
        ('delivered', 'Доставлен'),
    ]
    SHIPPING_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('courier', 'Курьер'),
        ('digital', 'Цифровая доставка'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    shipping_method = models.CharField(max_length=50, choices=SHIPPING_CHOICES, default='pickup')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} пользователя {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="euro")
    status = models.CharField(max_length=20, choices=[("pending", "Ожидание"), ("completed", "Завершено")])
    payment_link = models.URLField()
    transaction_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency}"