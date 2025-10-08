"""Settings for relational databases (DB).

The values are read from environmental variables or secret files.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.load_env_var import load_env_variable, load_json_env_variable

POSTGRESQL_DB_URL = 'postgresql+psycopg2://{u}:{p}@/{D}?host={h}'

POSTGRES_USER_CREDS = load_json_env_variable('POSTGRES_USER_CREDS')
user = POSTGRES_USER_CREDS.get('USER')
password = POSTGRES_USER_CREDS.get('PASSWORD')
host = load_env_variable('POSTGRES_HOST')
db = load_env_variable('POSTGRES_DB', default='fromScratchAPI')

postgres_url = POSTGRESQL_DB_URL.format(
	u=user,
	p=password,
	h=host,
	D=db,
)
print('--------------------------------')
print(postgres_url)

# Create the SQLAlchemy Engine for the connection to the DB.
engine = create_engine(postgres_url)
create_db_session = sessionmaker(
	autocommit=False,
	autoflush=False,
	bind=engine,
)
