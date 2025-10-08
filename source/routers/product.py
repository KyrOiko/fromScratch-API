from typing import Annotated
from uuid import UUID

from domain import Product, ProductCreate, ProductFilters
from fastapi import APIRouter, Depends, Request
from services.product.service import ProductService


class ProductRouter:
	"""Router for Product."""

	service = ProductService
	_filter = ProductFilters

	def __init__(self):
		self.router = APIRouter(prefix='/product', tags=['product'])
		self.router.add_api_route('', self.post, methods=['POST'])
		self.router.add_api_route('', self.delete, methods=['DELETE'])
		self.router.add_api_route('', self.put, methods=['PUT'])
		self.router.add_api_route('/{id}', self.get_one, methods=['GET'])
		self.router.add_api_route('', self.get_many, methods=['GET'])

	def post(self, request: Request, product: ProductCreate) -> Product:
		return self.service(request.state.db_session).add(product)

	def delete(self, request: Request, id: UUID) -> Product:
		_filter = self._filter(id=id)
		return self.service(request.state.db_session).delete(_filter)

	def put(self, request: Request, product: Product) -> Product:
		return self.service(request.state.db_session).update(product)

	def get_many(
		self, request: Request, filters: Annotated[ProductFilters, Depends()]
	) -> list[Product]:
		return self.service(request.state.db_session).get_many(filters)

	def get_one(self, request: Request, id: UUID) -> Product:
		_filter = self._filter(id=id)
		return self.service(request.state.db_session).get_one(_filter)
