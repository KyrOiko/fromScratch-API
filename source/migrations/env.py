"""Alembic env module."""

import sys
from logging.config import fileConfig
from pathlib import Path

import alembic_postgresql_enum  # noqa: F401
from alembic import context
from sqlalchemy import engine_from_config, pool, text

from models.base import Base
from settings.db import postgres_url

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)

config = context.config

config.set_main_option('sqlalchemy.url', postgres_url)

fileConfig(config.config_file_name)

target_metadata = Base.metadata
exclude_tables: list[str] = config.get_main_option('exclude', '').split(',')


def include_table(name, type_, parent_names):  # noqa: ARG001, ANN001
	"""What tables to include in the alembic migration."""
	return not (type_ == 'table' and name in exclude_tables)


def run_migrations_offline():
	"""Run migrations offline."""
	url = config.get_main_option('sqlalchemy.url')
	context.configure(
		url=url,
		target_metadata=target_metadata,
		literal_binds=True,
		dialect_opts={'paramstyle': 'named'},
		include_schemas=True,
	)

	with context.begin_transaction():
		context.run_migrations()


def run_migrations_online():
	"""Run migrations online."""
	connectable = engine_from_config(
		config.get_section(config.config_ini_section),
		prefix='sqlalchemy.',
		poolclass=pool.NullPool,
	)

	with connectable.connect() as connection:
		context.configure(
			connection=connection,
			target_metadata=target_metadata,
			include_schemas=True,
			include_name=include_table,
		)

		# Check docker-compose to understand why this path is used.
		with Path('../postgres/init.sql').open(encoding='utf-8') as file:
			query = text(file.read())
			connection.execute(query)

		schemas = {
			table.schema
			for table in target_metadata.sorted_tables
			if table.schema and table.schema != 'none'
		}
		for schema in schemas:
			connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schema}'))

		with context.begin_transaction():
			context.run_migrations()


if context.is_offline_mode():
	run_migrations_offline()
else:
	run_migrations_online()
