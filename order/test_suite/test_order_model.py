from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from order.models.order import Order
from product.models.product import Product
from product.models.category import Category

User = get_user_model()

class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.category = Category.objects.create(title="Ficção")

        self.prod1 = Product.objects.create(title="Livro A", price=Decimal("10.00"))
        self.prod1.category.add(self.category)

        self.prod2 = Product.objects.create(title="Livro B", price=Decimal("20.00"))
        self.prod2.category.add(self.category)

    def test_order_default_quantity_is_one(self):
        order = Order.objects.create(user=self.user)
        order.product.add(self.prod1)
        order.refresh_from_db()
        self.assertEqual(order.quantity, 1)

    def test_order_many_to_many_products(self):
        order = Order.objects.create(user=self.user)
        order.product.add(self.prod1, self.prod2)
        self.assertEqual(order.product.count(), 2)

    def test_order_user_association(self):
        order = Order.objects.create(user=self.user)
        order.product.add(self.prod1)
        self.assertEqual(order.user.username, "testuser")
