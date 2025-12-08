from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("id")

    def perform_create(self, serializer):
        # O teste envia "products_id"
        products_id = self.request.data.get("products_id", [])

        order = serializer.save()

        # Permite enviar um único ID ou lista
        if isinstance(products_id, int):
            products_id = [products_id]

        order.product.set(products_id)
