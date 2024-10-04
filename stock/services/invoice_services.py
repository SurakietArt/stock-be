from core.enum import Platform
from customer.models.customers_model import Customers
from stock.dataclass.invoice_dataclass import InvoiceParam
from stock.models.invoice import Invoice
from stock.services.sales_order_services import SalesOrderServices


class InvoiceServices:
    @classmethod
    def create_invoice(cls, param: InvoiceParam) -> Invoice:
        invoice_id = cls.generate_invoice_id()
        customer = Customers.objects.get(id=param.customer_id)
        sales_order = SalesOrderServices.create_sales_order(
            order_param=param.orders,
            platform=Platform.OTHER.value,
            customer=customer,
            date=param.date,
        )
        new_invoice = Invoice.objects.create(
            invoice_id=invoice_id,
            date=param.date,
            customer_id=param.customer_id,
            is_headquarter=param.is_headquarter,
            is_branch=param.is_branch,
            branch_num=param.branch_num,
            sales_order=sales_order,
            discount=param.discount,
        )
        return new_invoice

    @classmethod
    def generate_invoice_id(cls) -> str:
        """
        Generate invoice id from YYYYMMDDXXXX from running number
        :return:
        """
        pass
