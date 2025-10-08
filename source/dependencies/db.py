"""Dependencies for database."""

from domain.exceptions import (
	EntityAlreadyExists,
	EntityConstrainedCreationError,
	MissingFieldError,
)
from psycopg2 import errors
from sqlalchemy import Executable, Result
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session


def handle_integrity_error(db_session: Session, sql_e: DatabaseError):
	"""Handle integrity error, re-raising more specific exceptions."""
	try:
		if sql_e.orig:
			raise sql_e.orig
	except errors.ForeignKeyViolation as fkv:
		db_session.rollback()
		raise EntityConstrainedCreationError from fkv
	except errors.UniqueViolation as pkv:
		db_session.rollback()
		raise EntityAlreadyExists from pkv
	except errors.NotNullViolation as nv:
		db_session.rollback()
		raise MissingFieldError from nv


def commit_session(db_session: Session):
	"""Attempt to commit the database session.

	Args:
	    db_session: The database session to commit.

	Raises:
	    Exception: If an exception occurs while committing.
	"""
	try:
		db_session.commit()
	except DatabaseError as sql_e:
		handle_integrity_error(db_session, sql_e)


def execute_statement(db_session: Session, statement: Executable) -> Result:
	"""Attempt to execute an SQL statement.

	Args:
	    db_session: The db session to use while executing the statement.
	    statement: The SQL statement to execute.

	Raises:
	    Exception: If an exception occurs while executing the statement.
	"""
	try:
		return db_session.execute(statement)
	except DatabaseError as sql_e:
		handle_integrity_error(db_session, sql_e)
		db_session.rollback()
		raise
