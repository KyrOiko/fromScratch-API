from __future__ import annotations

from typing import TYPE_CHECKING

from models.base import Base, uuidpk
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
	from models import PurchaseORM


class CustomerORM(Base):
	__tablename__ = 'customer'

	id: Mapped[uuidpk]
	email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
	first_name: Mapped[str] = mapped_column(nullable=False)
	last_name: Mapped[str] = mapped_column(nullable=False)
	phone: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

	purchases: Mapped[list[PurchaseORM]] = relationship(back_populates='customer')
