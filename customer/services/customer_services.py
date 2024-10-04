from customer.dataclass.customer_dataclass import CustomerParam
from customer.models.customers_model import Customers


class CustomerService:
    @classmethod
    def get_or_create(cls, param: CustomerParam) -> Customers:
        if param.id is not None:
            customer = Customers.objects.get(id=param.id)
            return customer
        customer = Customers.objects.create(
            name=param.name,
            address=param.address,
            phone_number=param.phone_number,
            tax_id=param.tax_id,
        )
        return customer
