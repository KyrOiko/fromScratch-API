from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from models.base import Base, uuidpk
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
	from models import CustomerORM, ProductORM


class PurchaseORM(Base):
	__tablename__ = 'purchase'

	id: Mapped[uuidpk]
	customer_id: Mapped[UUID] = mapped_column(ForeignKey('customer.id'), nullable=False)
	total: Mapped[float] = mapped_column(nullable=False)
	customer: Mapped[CustomerORM] = relationship(back_populates='purchases')
	products: Mapped[list[ProductORM]] = relationship(secondary='purchase_product')
