from rest_framework import serializers
from order.models.order import Order
from product.serializers.product_serializer import ProductSerializer
from product.models.product import Product

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    products_id = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "product",
            "products_id",
            "quantity",
            "total",
        ]

    def create(self, validated_data):
        # Remove products_id antes de criar o Order
        products_id = validated_data.pop("products_id", [])

        # Cria o pedido sem o campo inválido
        order = Order.objects.create(**validated_data)

        # Associa os produtos
        if isinstance(products_id, int):
            products_id = [products_id]

        order.product.set(products_id)

        return order

    def get_total(self, obj):
        return sum([p.price for p in obj.product.all()])
