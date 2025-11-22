from django.test import TestCase
from .factories import OrderFactory


# Create your tests here.
class OrderSerializerTest(TestCase):
    def test_order_serializer_output(self):
        order = OrderFactory()
        from .serializers import OrderSerializer
        serializer = OrderSerializer(order)
        self.assertEqual(serializer.data['quantity'], order.quantity)

