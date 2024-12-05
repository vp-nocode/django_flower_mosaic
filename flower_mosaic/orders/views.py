from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Order, OrderItem
from catalog.models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json

@login_required
def create_order(request):

    if request.method == 'POST':

        cart = request.session.get('cart', {})
        print(f'cart: {cart}')
        if not cart:
            return redirect(reverse('create_order'))

        address = request.POST.get('address')
        order = Order.objects.create(user=request.user, delivery_address=address)

        for bouquet_id, quantity in cart.items():
            product = Product.objects.get(id=bouquet_id)
            print(f'product: {product}')
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        request.session['cart'] = {}
        return redirect(reverse('order_list'))

    else:

        cart = request.session.get('cart', {})
        products = []
        for bouquet_id, quantity in cart.items():
            product = Product.objects.get(id=bouquet_id)
            products.append({
                'product': product,
                'name': product.name,
                'id': product.id,
                'quantity': quantity,
                'price': product.price,
                'total_price': product.price * quantity
            })

        print(f"Products: {products}")
        return render(request, 'orders/create_order.html', {'products': products})


def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


@require_POST
def update_cart(request):
    data = json.loads(request.body)
    print(f'data: {data}')
    product_id = str(data.get('product_id'))
    quantity = int(data.get('quantity'))

    cart = request.session.get('cart', {})
    print(f'before cart: {cart}')
    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id, None)  # Удалить товар, если количество равно 0

    print(f'after cart: {cart}')
    request.session['cart'] = cart

    return JsonResponse({'success': True})
