"""Config file for tests."""

import asyncio
import inspect
from functools import wraps
from os import environ
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from main import app
from models.base import Base
from settings.db import create_db_session
from sqlalchemy import text
from sqlalchemy_continuum import versioning_manager

if environ['ENVIRONMENT'] == 'production':
	msg = 'Invalid environment or environment not set'
	raise ValueError(msg)

postgres_session = create_db_session()
versioning_manager.track_session(postgres_session)


def session_factory_for_factories():
	postgres_session.rollback()
	return postgres_session


def clear_data(session):
	meta = Base.metadata
	for table in reversed(meta.sorted_tables):
		schema_name = table.schema if table.schema else 'public'
		session.execute(text(f'DELETE FROM {schema_name}.{table.name}'))
		session.commit()

	# SQL Files that need to run because we're truncating the tables.
	# sql_dir = '/postgres/sql'
	# sql_files = [
	# 	'000-iam-permissions.sql',
	# 	'001-iam-predefined-roles.sql',
	# ]
	# for sql_file in sql_files:
	# 	with Path(f'{sql_dir}/{sql_file}').open(encoding='utf-8') as file:
	# 		query = text(file.read())
	# 	session.execute(query)

	session.commit()


def pytest_sessionstart(session):  # noqa: ARG001
	"""Runs at the start of the pytest session.

	Rollback and clear data.
	"""
	versioning_manager.track_session(postgres_session)
	postgres_session.rollback()
	clear_data(postgres_session)


@pytest.fixture(autouse=True)
def _setup_run_teardown():
	"""Setup and teardown for the module."""
	postgres_session.rollback()
	clear_data(postgres_session)
	yield
	postgres_session.rollback()
	clear_data(postgres_session)
	postgres_session.close()


@pytest.fixture(scope='session')
def client():
	with TestClient(app) as c:
		yield c


@pytest.fixture(scope='session')
def event_loop():
	try:
		loop = asyncio.get_running_loop()
	except RuntimeError:
		loop = asyncio.new_event_loop()
	yield loop
	loop.close()


@pytest.mark.asyncio()
def async_step(step):
	"""Convert an async step function to a normal one."""
	signature = inspect.signature(step)
	parameters = list(signature.parameters.values())
	has_event_loop = any(parameter.name == 'event_loop' for parameter in parameters)
	if not has_event_loop:
		parameters.append(
			inspect.Parameter(
				'event_loop',
				inspect.Parameter.POSITIONAL_OR_KEYWORD,
			),
		)
		step.__signature__ = signature.replace(parameters=parameters)

	@wraps(step)
	def run_step(*args, **kwargs):
		loop = kwargs['event_loop'] if has_event_loop else kwargs.pop('event_loop')
		return loop.run_until_complete(step(*args, **kwargs))

	return run_step


def parse_bool_string(value: str) -> bool:
	"""Parse a string to a boolean."""
	return value.lower() in {'true', '1'}
