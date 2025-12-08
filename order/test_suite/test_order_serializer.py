from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from order.models.order import Order
from product.models.product import Product
from product.models.category import Category
from order.serializers.order_serializer import OrderSerializer

User = get_user_model()

class OrderSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="serializer_user", password="pass")
        self.cat = Category.objects.create(title="Biografia")

        self.prod = Product.objects.create(title="Livro Bio", price=Decimal("25.00"))
        self.prod.category.add(self.cat)

        self.order = Order.objects.create(user=self.user)
        self.order.product.add(self.prod)

    def test_order_serializer_outputs_expected_fields(self):
        serializer = OrderSerializer(instance=self.order)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("user", data)
        self.assertIn("product", data)
        self.assertIn("quantity", data)

    def test_order_serializer_product_list_not_empty(self):
        serializer = OrderSerializer(instance=self.order)
        data = serializer.data
        self.assertTrue(len(data.get("product", [])) >= 1)

    def test_serializer_serialized_user_matches(self):
        serializer = OrderSerializer(instance=self.order)
        data = serializer.data
        self.assertIn(str(self.user.pk), str(data.get("user", "")))
