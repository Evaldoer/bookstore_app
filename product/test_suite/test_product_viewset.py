import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory
from product.models.product import Product

class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        token.save()

        self.category = CategoryFactory()
        self.product = ProductFactory(title="pro controller", price=200, categories=[self.category])

    def authenticate(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_all_products(self):
        self.authenticate()
        response = self.client.get(reverse("product-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["results"][0]["title"], self.product.title)

    def test_get_single_product(self):
        self.authenticate()
        response = self.client.get(reverse("product-detail", kwargs={"version": "v1", "pk": self.product.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["title"], self.product.title)

    def test_create_product(self):
        self.authenticate()
        new_category = CategoryFactory()
        data = json.dumps({"title": "notebook", "price": 800.00, "categories_id": [new_category.id]})
        response = self.client.post(reverse("product-list", kwargs={"version": "v1"}), data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(title="notebook").exists())

    def test_delete_product(self):
        self.authenticate()
        response = self.client.delete(reverse("product-detail", kwargs={"version": "v1", "pk": self.product.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
