from pymongo import AsyncMongoClient
from pymongo.database import Database as MongoDatabase

from ..config import EnvironmentVariables

env = EnvironmentVariables()
DATABASE_URL = env.database_url
DATABASE = env.database

class Database:
    def __init__(self, database_url=DATABASE_URL):
        self.database_url = database_url
        self.client = AsyncMongoClient(self.database_url)
        self.database: MongoDatabase = self.client[DATABASE]


# Create a database instance
database = Database()

# Dependency to get the DB session
def get_db():
    return database.database
