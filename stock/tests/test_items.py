import pytest
from rest_framework import status
from rest_framework.test import APIClient

from stock.models.category_model import Category
from stock.models.items_model import Items
from stock.models.units_model import Units


@pytest.mark.django_db
class TestItemsAPI:
    def setup_method(self):
        self.base_url = "/api/v1/stock/items"
        self.client = APIClient()
        self.unit = Units.objects.create(name="Test Unit")
        self.category = Category.objects.create(name="Test Category")
        self.item = Items.objects.create(
            name="Test Item",
            amount=10,
            price_per_unit=10.0,
            unit=self.unit,
            category=self.category,
        )

    def test_create_item(self):
        data = {
            "name": "New Item",
            "amount": 5,
            "price_per_unit": 10.0,
            "unit_id": self.unit.id,
            "category_id": self.category.id,
        }
        response = self.client.post(self.base_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Items.objects.filter(name="New Item").exists()

    def test_read_item(self):
        url = f"{self.base_url}/{self.item.id}"  # Adjust based on your URL structure
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Test Item"

    def test_update_item(self):
        url = f"{self.base_url}/{self.item.id}"  # Adjust based on your URL structure
        data = {
            "name": "Updated Item",
            "amount": 20,
            "price_per_unit": 7.5,
            "unit_id": self.unit.id,
            "category_id": self.category.id,
        }
        response = self.client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        self.item.refresh_from_db()
        assert self.item.name == "Updated Item"
        assert self.item.amount == 20

    def test_delete_item(self):
        url = f"{self.base_url}/{self.item.id}"  # Adjust based on your URL structure
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Items.objects.filter(id=self.item.id).exists()
