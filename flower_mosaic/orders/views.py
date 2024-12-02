from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Order, OrderItem
from catalog.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def create_order(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('products')
        quantities = request.POST.getlist('quantities')
        products = Product.objects.filter(id__in=product_ids)
        # address = request.user.address
        address = request.POST.get('address')
        order = Order.objects.create(user=request.user, delivery_address=address)

        for product, quantity in zip(products, quantities):
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=int(quantity),
                price=product.price
            )

        return redirect(reverse('order_list'))
    else:
        products = Product.objects.all()
        return render(request, 'orders/create_order.html', {'products': products})


def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})
