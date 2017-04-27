import os
from peewee import Model, CharField, PostgresqlDatabase
from playhouse.postgres_ext import ArrayField
from playhouse.db_url import connect

import settings

psql_db = PostgresqlDatabase(
	settings.DB_NAME,
	user = settings.DB_USER,
	password=settings.DB_PASS,
	host=settings.DB_HOST,
	)

if os.environ.get('DATABASE_URL'):
	database = connect(os.environ.get('DATABASE_URL'))
else:
	database = psql_db

class BaseModel(Model):
	class Meta:
		database = database


class SynsAnts(BaseModel):
	word = CharField()
	synonyms = ArrayField(CharField, default=[])
	antonyms = ArrayField(CharField, default=[])
