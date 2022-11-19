import psycopg2 as pg2
import os, sys
from database_credentials import credentials

print(f'\n\n\nTrying to connect to {os.environ.get("POSTGRES_HOST")}\n\n\n', file=sys.stderr)

conn = pg2.connect(
	database = os.environ.get('POSTGRES_DB'),
	user = os.environ.get('POSTGRES_USER'),
	password = os.environ.get('POSTGRES_PASSWORD'),
	host = os.environ.get('POSTGRES_HOST'),
	port = os.environ.get('POSTGRES_PORT')
)

print('Connection status: ', conn.closed, file=sys.stderr, flush=True)