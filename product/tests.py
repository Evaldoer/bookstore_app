from django.test import TestCase

from product.factories import ProductFactory
from product.serializers.product_serializer import ProductSerializer


# Create your tests here.
class ProductSerializerTest(TestCase):
    def test_product_serializer_output(self):
        product = ProductFactory()
        serializer = ProductSerializer(product)
        # Agora verificamos 'title' em vez de 'name'
        self.assertIn("title", serializer.data)
        self.assertEqual(serializer.data["title"], product.title)