from .customer.mapper import CustomerCreateMapper, CustomerMapper
from .product.mapper import ProductCreateMapper, ProductMapper
from .purchase.mapper import PurchaseCreateMapper, PurchaseMapper

customer_orm_schema_mapper = CustomerMapper()
customer_schema_orm_mapper = CustomerCreateMapper()

product_orm_schema_mapper = ProductMapper()
product_schema_orm_mapper = ProductCreateMapper()

purchase_orm_schema_mapper = PurchaseMapper(customer_orm_schema_mapper, product_orm_schema_mapper)
purchase_schema_orm_mapper = PurchaseCreateMapper()
