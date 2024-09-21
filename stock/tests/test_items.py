from rest_framework import status
from rest_framework.test import APITestCase

from stock.models.category_model import Category
from stock.models.items_model import Items
from stock.models.units_model import Units


class ItemsTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.unit = Units.objects.create(name="Test Unit")
        self.item = Items.objects.create(
            name="Test Item",
            amount=10,
            price=100.0,
            price_per_unit=10.0,
            unit=self.unit,
            category=self.category,
        )

    def test_create_item(self):
        url = "/api/v1/items"
        data = {
            "name": "New Item",
            "amount": 5,
            "price": 50.0,
            "price_per_unit": 10.0,
            "unit": self.unit.id,
            "category": self.category.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Items.objects.filter(name="New Item").exists())

    def test_read_item(self):
        url = f"/api/v1/items/{self.item.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Item")

    def test_update_item(self):
        url = f"/api/v1/items/{self.item.id}"
        data = {
            "name": "Updated Item",
            "amount": 20,
            "price": 150.0,
            "price_per_unit": 7.5,
            "unit": self.unit.id,
            "category": self.category.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated Item")
        self.assertEqual(self.item.amount, 20)

    def test_delete_item(self):
        url = f"/api/v1/items/{self.item.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Items.objects.filter(id=self.item.id).exists())
