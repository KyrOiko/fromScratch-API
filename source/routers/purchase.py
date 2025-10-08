from typing import Annotated
from uuid import UUID

from domain import Purchase, PurchaseCreate, PurchaseFilters
from fastapi import APIRouter, Depends, Request
from services.purchase.service import PurchaseService


class PurchaseRouter:
	"""Router for Purchase."""

	service = PurchaseService
	_filter = PurchaseFilters

	def __init__(self):
		self.router = APIRouter(prefix='/purchase', tags=['purchase'])
		self.router.add_api_route('', self.post, methods=['POST'])
		self.router.add_api_route('', self.delete, methods=['DELETE'])
		self.router.add_api_route('', self.put, methods=['PUT'])
		self.router.add_api_route('/{id}', self.get_one, methods=['GET'])
		self.router.add_api_route('', self.get_many, methods=['GET'])

	def post(self, request: Request, purchase: PurchaseCreate) -> Purchase:
		return self.service(request.state.db_session).add(purchase)

	def delete(self, request: Request, id: UUID) -> Purchase:
		_filter = self._filter(id=id)
		return self.service(request.state.db_session).delete(_filter)

	def put(self, request: Request, purchase: Purchase) -> Purchase:
		return self.service(request.state.db_session).update(purchase)

	def get_many(
		self, request: Request, filters: Annotated[PurchaseFilters, Depends()]
	) -> list[Purchase]:
		return self.service(request.state.db_session).get_many(filters)

	def get_one(self, request: Request, id: UUID) -> Purchase:
		_filter = self._filter(id=id)
		return self.service(request.state.db_session).get_one(_filter)
