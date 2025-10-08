"""SecretManager module."""

import json
from os import environ
from typing import Any


def load_json_env_variable(
	env_var_name: str,
	default: Any = None,
	*,
	required: bool = True,
) -> dict[str, str]:
	"""Load a JSON environment variable.

	Args:
	    env_var_name: The name of the environment variable to load.
	    default: The default value for the environment variable.
	    required: Whether the environment variable is required.

	Returns:
	    The value of the environment variable.

	Raises:
	    TypeError: If the environment variable is not a JSON.
	"""
	loaded_env_var = load_env_variable(env_var_name, default, required=required)

	if not isinstance(loaded_env_var, str):
		msg = f'Environment variable {env_var_name} is not a JSON!'
		raise TypeError(msg)

	return json.loads(loaded_env_var)


def load_env_variable(
	env_var_name: str,
	default: Any = None,
	*,
	required: bool = True,
) -> str:
	"""Load a single environment variable.

	Args:
	    env_var_name: The name of the environment variable to load.
	    default: The default value for the environment variable.
	    required: Whether the environment variable is required.

	Returns:
	    The value of the environment variable.

	Raises:
	    ValueError: If the environment variable is not found and is also
	        required.
	"""
	loaded_env_var = environ.get(env_var_name, default)

	if not loaded_env_var and required:
		msg = f'Environment variable {env_var_name} is missing!'
		raise ValueError(msg)

	return loaded_env_var
