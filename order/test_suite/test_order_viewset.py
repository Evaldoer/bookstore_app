import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory
from product.models.product import Product
from order.models.order import Order

class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        token.save()

        self.category = CategoryFactory(title="tech")
        self.product = ProductFactory(title="mouse", price=100, category=[self.category])
        self.order = Order.objects.create(user=self.user)
        self.order.product.add(self.product)

    def authenticate(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_order_list(self):
        self.authenticate()
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["results"][0]["product"][0]["title"], self.product.title)

    def test_create_order(self):
        self.authenticate()
        new_product = ProductFactory()
        data = json.dumps({"products_id": [new_product.id], "user": self.user.id})
        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.filter(user=self.user, product=new_product).exists())

    def test_get_order_detail(self):
        self.authenticate()
        response = self.client.get(reverse("order-detail", kwargs={"version": "v1", "pk": self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["total"], self.product.price)
