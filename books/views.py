import razorpay
from razorpay.errors import SignatureVerificationError
from django.conf import settings
from django.shortcuts import render, get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Order, Payment, Book, OrderItem

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "books/book_details.html", {"book": book})   

def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        order = get_object_or_404(Order, order_id=order_id)
        order_items = order.items.all()
        
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            payment = Payment.objects.create(
                order=order,
                provider_payment_id=payment_id,
                amount=order.total_amount,
                status='SUCCESS'
            )
            for item in order_items:
                book = item.book
            if book.stock >= item.quantity:
                book.stock -= item.quantity
                book.save()
            else:
                book.stock = 0
            order.save()
            
            return redirect('payment_success_page', pk=payment.pk)

        except SignatureVerificationError:
            payment = Payment.objects.create(
                order=order,
                razorpay_payment_id=payment_id,
                amount=order.total_amount,
                status='FAILED'
            )
            return redirect('payment_failed_page', pk=payment.pk)   


def payment_success_page(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    order = payment.order
    order_items = order.items.all()
    return render(request, "books/payment_success.html", {"payment": payment,"order_items": order_items})


def payment_failed_page(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, "books/payment_failed.html", {"payment": payment})

def checkout(request, pk):
    book = get_object_or_404(Book, id=pk)
    quantity = int(request.GET.get('quantity', 1))
    
    amount = int(book.price * 100)
    total_amount = book.price * quantity

    razorpay_order = client.order.create({
        "amount": amount*quantity,
        "currency": "INR",
        "payment_capture": "1"
    })

    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount,
        order_id=razorpay_order["id"]
    )

    OrderItem.objects.create(
        order=order,
        book=book,
        quantity=quantity,
        price=book.price
    )

    context = {
        "book": book,
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "total_amount":total_amount,
        "quantity":quantity,
        "currency": "INR",
        "order": order
    }
    return render(request, "books/checkout.html", context)