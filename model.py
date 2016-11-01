from peewee import Model, CharField
from playhouse.postgres_ext import ArrayField
from playhouse.pool import PostgresqlExtDatabase

import settings

psql_db = PostgresqlExtDatabase(
	settings.DB_NAME,
	user = settings.DB_USER,
	password=settings.DB_PASS,
	host=settings.DB_HOST,
	register_hstore=False
	)

class BaseModel(Model):
	class Meta:
		database = psql_db


class SynsAnts(BaseModel):
	word = CharField()
	synonyms = ArrayField(CharField, default=[])
	antonyms = ArrayField(CharField, default=[])
