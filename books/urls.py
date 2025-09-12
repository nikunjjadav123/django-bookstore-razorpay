
from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("book/<int:pk>/", views.book_detail, name="book_detail"),
    path('checkout/<int:pk>/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path("payment/success/<int:pk>/", views.payment_success_page, name="payment_success_page"),
    path("payment/failed/<int:pk>/", views.payment_failed_page, name="payment_failed_page"),
]

