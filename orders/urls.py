from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('order/', views.OrderCreateView.as_view(), name='order'),
    path('order/success/', views.OrderSuccessView.as_view(), name='success'),
    path('order/cancel/', views.OrderCancelView.as_view(), name='cancel'),
    path('order/orders', views.OrdersView.as_view(), name='orders'),
    path('order/orders/order-detail/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
]
