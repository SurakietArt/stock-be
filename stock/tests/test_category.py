import pytest
from rest_framework import status
from rest_framework.test import APIClient

from stock.models.category_model import Category


@pytest.mark.django_db
class TestCategoryAPI:
    def setup_method(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")

    def test_create_category(self):
        url = "/api/v1/categories"  # Adjust based on your URL structure
        data = {"name": "New Category"}
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="New Category").exists()

    def test_read_category(self):
        url = f"/api/v1/categories/{self.category.id}"  # Adjust based on your URL structure
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Test Category"

    def test_update_category(self):
        url = f"/api/v1/categories/{self.category.id}"  # Adjust based on your URL structure
        data = {"name": "Updated Category"}
        response = self.client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        self.category.refresh_from_db()
        assert self.category.name == "Updated Category"

    def test_delete_category(self):
        url = f"/api/v1/categories/{self.category.id}"  # Adjust based on your URL structure
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Category.objects.filter(id=self.category.id).exists()
