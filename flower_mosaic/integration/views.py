from rest_framework.decorators import api_view
from rest_framework.response import Response
from orders.models import Order, OrderItem
from rest_framework import serializers

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    image = serializers.CharField(source='product.image')

    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'price', 'total_price', 'image']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'order_date', 'delivery_address', 'items']
        #fields = ['id', 'status', 'order_date', 'delivery_address']

@api_view(['GET'])
def order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        print(f'order: {order}')
        serializer = OrderSerializer(order)
        print(f'serializer: {serializer}')
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=404)




'''
@api_view(['GET'])
def order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        print(f'order: {order}')
        items = OrderItem.objects.filter(order=order)
        print(f'items: {items}')
        order_data = {
            'order_id': order.id,
            'status': order.status,
            #'created_at': order.created_at,
            'order_date': order.order_date,
            'delivery_address': order.delivery_address,
            'items': [{
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': item.price,
                'total_price': item.total_price,
                'image': item.product.image,
            } for item in items]
        }
        print(f'order_data: {order_data}')
        return Response(order_data)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=404)
'''
