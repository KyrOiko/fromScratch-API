from uuid import UUID

from models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class PurchaseProductORM(Base):
	__tablename__ = 'purchase_product'

	purchase_id: Mapped[UUID] = mapped_column(
		ForeignKey('purchase.id', ondelete='CASCADE'), primary_key=True
	)
	product_id: Mapped[UUID] = mapped_column(
		ForeignKey('product.id', ondelete='CASCADE'), primary_key=True
	)
