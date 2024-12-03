from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='catalog'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
