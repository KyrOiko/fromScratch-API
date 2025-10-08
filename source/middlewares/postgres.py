"""PostgreSQL Middleware."""

from sqlalchemy.orm import Session, scoped_session
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from settings.db import create_db_session


class PostgreSQLMiddleware:
	"""PostgreSQL Middleware."""

	def __init__(self, app: ASGIApp) -> None:
		"""Initialize the middleware."""
		self.app = app

	async def __call__(self, scope: Scope, receive: Receive, send: Send):
		"""Entrypoint of the middleware."""
		# Required for the lifespan of ASGI to not complain.
		if scope['type'] != 'http':
			return await self.app(scope, receive, send)

		request = Request(scope)
		db_session: Session = scoped_session(
			create_db_session,
			scopefunc=lambda: request,
		)()
		request.state.db_session = db_session

		await self.app(scope, receive, send)
		db_session.close()
		return None
