from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

def generate_order_id():
    return uuid.uuid4().hex.upper()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=200, blank=True)
    book_image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # currency units
    sku = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    STATUS_CHOICES = [
        ('created','Created'),
        ('pending','Pending Payment'),
        ('paid','Paid'),
        ('failed','Failed'),
        ('cancelled','Cancelled'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.CharField(max_length=100, unique=True, default=generate_order_id)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='INR')  # or 'USD'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def line_total(self):
        return self.price * self.quantity

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    provider = models.CharField(max_length=50)  # 'razorpay' or 'stripe'
    provider_payment_id = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=50, default='initiated')
    created_at = models.DateTimeField(auto_now_add=True)
    raw_response = models.JSONField(default=dict, blank=True)
