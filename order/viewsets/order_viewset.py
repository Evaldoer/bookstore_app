from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from order.models import Order
from order.serializers import OrderSerializer
from product.models.product import Product

class OrderViewSet(ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("id")

    # ✅ REMOVA o método list() — deixe o DRF paginar sozinho

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        products_id = request.data.get("products_id", [])

        order = Order.objects.create(user=request.user)

        for pid in products_id:
            product = Product.objects.get(id=pid)
            order.product.add(product)

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)