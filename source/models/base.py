"""Base of all models."""

import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
	"""Base class for all models."""

	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		onupdate=func.now(),
	)


intpk = Annotated[int, mapped_column(primary_key=True)]
uuidpk = Annotated[
	uuid.UUID,
	mapped_column(primary_key=True, default=uuid.uuid4, server_default=text('gen_random_uuid()')),
]
