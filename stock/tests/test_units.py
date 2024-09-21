import pytest
from rest_framework import status
from rest_framework.test import APIClient

from stock.models.units_model import Units


@pytest.mark.django_db
class TestUnitsAPI:
    def setup_method(self):
        self.client = APIClient()
        self.unit = Units.objects.create(name="Test Unit")

    def test_create_unit(self):
        url = "/api/v1/units"  # Adjust based on your URL structure
        data = {"name": "New Unit"}
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Units.objects.filter(name="New Unit").exists()

    def test_read_unit(self):
        url = f"/api/v1/units/{self.unit.id}"  # Adjust based on your URL structure
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Test Unit"

    def test_update_unit(self):
        url = f"/api/v1/units/{self.unit.id}"  # Adjust based on your URL structure
        data = {"name": "Updated Unit"}
        response = self.client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        self.unit.refresh_from_db()
        assert self.unit.name == "Updated Unit"

    def test_delete_unit(self):
        url = f"/api/v1/units/{self.unit.id}"  # Adjust based on your URL structure
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Units.objects.filter(id=self.unit.id).exists()
