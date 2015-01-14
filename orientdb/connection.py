import pyorient

from config import settings


db_client = pyorient.OrientDB(settings.DB_HOST, int(settings.DB_PORT))
db_client.connect(settings.DB_USER, settings.DB_PASS)

if not db_client.db_exists(settings.DB_NAME, settings.DB_STORAGE_TYPE):
    db_client.db_create(settings.DB_NAME,
                        settings.DB_TYPE,
                        settings.DB_STORAGE_TYPE)

db_client.db_open(settings.DB_NAME, settings.DB_USER, settings.DB_PASS)
