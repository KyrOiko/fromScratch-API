from __future__ import annotations

from models.base import Base, uuidpk
from sqlalchemy.orm import Mapped, mapped_column


class ProductORM(Base):
	__tablename__ = 'product'

	id: Mapped[uuidpk]
	name: Mapped[str] = mapped_column(nullable=False)
	description: Mapped[str] = mapped_column(nullable=False)
	price: Mapped[float] = mapped_column(nullable=False)
