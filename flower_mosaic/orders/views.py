from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Order, OrderItem
from catalog.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def create_order(request):

    if request.method == 'POST':

        cart = request.session.get('cart', {})
        if not cart:
            return redirect(reverse('create_order'))

        address = request.POST.get('address')
        order = Order.objects.create(user=request.user, delivery_address=address)

        for bouquet_id, quantity in cart.items():
            product = Product.objects.get(id=bouquet_id)
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


# @login_required
# def create_order(request):
#     if request.method == 'POST':
#         cart_json = request.POST.get('cart', '{}')  # Используйте '{}' как значение по умолчанию
#         try:
#             cart = json.loads(cart_json)
#         except json.JSONDecodeError:
#             return HttpResponseBadRequest("Invalid cart data")
#         address = request.POST.get('address')
#         order = Order.objects.create(user=request.user, delivery_address=address)
#
#         for bouquet_id, quantity in cart.items():
#             product = Product.objects.get(id=bouquet_id)
#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 quantity=quantity,
#                 price=product.price
#             )
#
#         # Очистка корзины после создания заказа
#         # request.POST['cart'] = '{}'
#         return redirect(reverse('order_list'))
#
#     else:
#         # return render(request, 'orders/create_order.html')
#         return HttpResponseBadRequest("This view only handles POST requests.")

# @login_required
# def create_order(request):
#     if request.method == 'POST':
#         product_ids = request.POST.getlist('products')
#         quantities = request.POST.getlist('quantities')
#         products = Product.objects.filter(id__in=product_ids)
#         # address = request.user.address
#         address = request.POST.get('address')
#         order = Order.objects.create(user=request.user, delivery_address=address)
#
#         for product, quantity in zip(products, quantities):
#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 quantity=int(quantity),
#                 price=product.price
#             )
#
#         return redirect(reverse('order_list'))
#     else:
#         # products = Product.objects.all()
#         # return render(request, 'orders/create_order.html', {'products': products})
#         return render(request, 'orders/create_order.html')
#



def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})
