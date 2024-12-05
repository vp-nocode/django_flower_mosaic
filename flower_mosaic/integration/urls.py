from django.urls import path
from . import views

urlpatterns = [
    path('order_status/<int:order_id>/', views.order_status, name='order_status'),
]
