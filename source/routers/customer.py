from typing import Annotated
from uuid import UUID

from domain import Customer, CustomerCreate, CustomerFilters
from fastapi import APIRouter, Depends, Request
from services.customer.service import CustomerService


class CustomerRouter:
	"""Router for Customer."""

	service = CustomerService
	_filter = CustomerFilters

	def __init__(self):
		self.router = APIRouter(prefix='/customer', tags=['customer'])
		self.router.add_api_route('', self.post, methods=['POST'])
		self.router.add_api_route('', self.delete, methods=['DELETE'])
		self.router.add_api_route('', self.put, methods=['PUT'])
		self.router.add_api_route('/{id}', self.get_one, methods=['GET'])
		self.router.add_api_route('', self.get_many, methods=['GET'])

	def post(self, request: Request, customer: CustomerCreate) -> Customer:
		return self.service(request.state.db_session).add(customer)

	def delete(self, request: Request, id: UUID) -> Customer:
		_filter = self._filter(id=id)
		return self.service(request.state.db_session).delete(_filter)

	def put(self, request: Request, customer: Customer) -> Customer:
		return self.service(request.state.db_session).update(customer)

	def get_many(
		self, request: Request, filters: Annotated[CustomerFilters, Depends()]
	) -> list[Customer]:
		return self.service(request.state.db_session).get_many(filters)

	def get_one(self, request: Request, id: UUID) -> Customer:
		_filter = self._filter(id=id)
		return self.service(request.state.db_session).get_one(_filter)
