from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from order.factories import OrderFactory, UserFactory
from product.factories import ProductFactory

class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory()
        self.order = OrderFactory(user=self.user, product=[self.product])

    def test_list_orders(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_order(self):
        response = self.client.get(reverse("order-detail", kwargs={"version": "v1", "pk": self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        data = {"products_id": [self.product.id], "user": self.user.id}
        response = self.client.post(reverse("order-list", kwargs={"version": "v1"}), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_order(self):
        data = {"products_id": [self.product.id], "user": self.user.id, "quantity": 5}
        response = self.client.put(reverse("order-detail", kwargs={"version": "v1", "pk": self.order.id}), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], 5)

    def test_partial_update_order(self):
        data = {"quantity": 10}
        response = self.client.patch(reverse("order-detail", kwargs={"version": "v1", "pk": self.order.id}), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], 10)

    def test_delete_order(self):
        response = self.client.delete(reverse("order-detail", kwargs={"version": "v1", "pk": self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_total_field(self):
        response = self.client.get(reverse("order-detail", kwargs={"version": "v1", "pk": self.order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], self.product.price * self.order.quantity)