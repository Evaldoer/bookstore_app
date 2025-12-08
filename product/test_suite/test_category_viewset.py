from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

from product.factories import CategoryFactory
from product.models import Category

class CategoryViewSetTests(APITestCase):
    client = APIClient()

    def setUp(self):
        # Cria uma categoria de teste usando factory
        self.category = CategoryFactory(title="books")

    def test_get_all_categories(self):
        response = self.client.get(reverse("category-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        category_data = response.json()
        self.assertTrue("results" in category_data)
        self.assertEqual(category_data["results"][0]["title"], self.category.title)

    def test_create_category(self):
        data = {"title": "technology"}
        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}),
            data=data,
            format="json",  # Use format json para DRF
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(title="technology")
        self.assertEqual(created_category.title, "technology")

    def test_delete_category(self):
        category_id = self.category.id
        response = self.client.delete(
            reverse("category-detail", kwargs={"version": "v1", "pk": category_id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Certifica que realmente foi deletada
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=category_id)
