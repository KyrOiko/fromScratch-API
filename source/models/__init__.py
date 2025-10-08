"""ORM Models Module."""

from sqlalchemy.orm import configure_mappers

# Import all models to ensure they are registered with SQLAlchemy
from .customer import CustomerORM
from .product import ProductORM
from .purchase import PurchaseORM
from .purchase_product import PurchaseProductORM

configure_mappers()
