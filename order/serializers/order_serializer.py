from rest_framework import serializers
from order.models import Order
from product.serializers.product_serializer import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        # soma os preços de todos os produtos do pedido
        total = sum([product.price for product in instance.product.all()])
        return total

    class Meta:
        model = Order   # ✅ aqui estava errado, precisa ser Order
        fields = ['id', 'user', 'product', 'quantity', 'total']