import pytest
from rest_framework import status
from rest_framework.test import APIClient

from customer.models.customers_model import Customers


@pytest.mark.django_db
class TestCustomerAPI:
    def setup_method(self):
        self.base_url = "/api/v1/customers/"
        self.client = APIClient()
        self.customer_data = {
            "name": "Art Surakiet",
            "nick_name": "Johnny",
            "address": "1234 Main St, Springfield",
            "phone_number": "555-1234",
            "tax_id": "123-456-789",
        }
        self.customer = Customers.objects.create(**self.customer_data)

    def test_create_customer(self):
        url = self.base_url
        response = self.client.post(url, self.customer_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == self.customer_data["name"]
        assert response.data["nick_name"] == self.customer_data["nick_name"]
        assert response.data["address"] == self.customer_data["address"]
        assert response.data["phone_number"] == self.customer_data["phone_number"]
        assert response.data["tax_id"] == self.customer_data["tax_id"]

    def test_read_customer(self):
        url = f"{self.base_url}{self.customer.id}"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == self.customer_data["name"]

    def test_update_customer(self):
        url = f"{self.base_url}{self.customer.id}"
        data = {"name": "Updated Customer"}
        response = self.client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        self.customer.refresh_from_db()
        assert self.customer.name == "Updated Customer"

    def test_delete_customer(self):
        url = f"{self.base_url}{self.customer.id}"
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Customers.objects.filter(id=self.customer.id).exists()
