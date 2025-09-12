from django.contrib import admin
from .models import Book, Order, OrderItem,Payment   

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'total_amount', 'status', 'created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'book', 'quantity', 'price']

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]
    list_display = ['id', 'user', 'total_amount', 'is_paid', 'created_at']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'provider_payment_id', 'amount', 'status', 'created_at']
 
# admin.site.register(Book)
# admin.site.register(Order, OrderAdmin)
# admin.site.register(Payment, PaymentAdmin)