import os
from abc import ABC, abstractmethod

from pymongo import MongoClient

from extensions.python_exceptions import MultipleObjectsReturned

# ====================================================
# =                   Interfaces                     =
# ====================================================


class MongoCollectionInterface(ABC):

    @abstractmethod
    def _get_or_create_collection(self, collection_name: str):
        pass

    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        pass


class MongoDocumentInterface(ABC):

    @abstractmethod
    def all(self) -> dict:
        pass

    @abstractmethod
    def create(self, **kwargs) -> None:
        pass

    @abstractmethod
    def get(self, **kwargs) -> dict:
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def update(self, **kwargs) -> None:
        pass

    @abstractmethod
    def delete(self, **kwargs) -> None:
        pass

# ====================================================
# =                     Classes                      =
# ====================================================


class Mongo:
    CLIENT = MongoClient(os.getenv('MONGO_DB_URL'))

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Mongo, cls).__new__(cls)
        return cls.instance

    def __init__(self, *args, **kwargs):
        self.db = self.CLIENT[os.getenv('MONGO_DB_NAME')]


class Collection(MongoCollectionInterface):

    mongo = Mongo()

    def _get_or_create_collection(self, collection_name: str = None):
        if not collection_name:
            collection_name = self.__class__.__name__

        return self.mongo.db[collection_name]

    def collection_exists(self, collection_name: str) -> bool:
        return self.mongo.db.collection_exists(collection_name)


class Document(Collection, MongoDocumentInterface):

    def __init__(self, collection_name: str, **kwargs):
        self.collection = self._get_or_create_collection(collection_name)

    def all(self):
        return list(self.collection.find())

    def create(self, **kwargs) -> None:
        self.collection.insert_one(kwargs)

    def get(self, **kwargs) -> dict:
        result = list(self.collection.find(kwargs))
        if len(result) > 1:
            raise MultipleObjectsReturned(f"get method have to return only one result but get {len(result)}")

        return self.collection.find_one(kwargs)

    def count(self, **kwargs) -> int:
        return self.collection.count_documents(kwargs)

    def update(self,query, **kwargs) -> None:
        self.collection.update_one(query, kwargs)

    def delete(self, **kwargs) -> None:
        self.collection.delete_one(kwargs)



