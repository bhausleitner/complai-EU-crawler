import logging

import pymongo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        logger.info(f"Created MongoClient for {self.mongo_uri}")

    def process_item(self, item, id_key):
        # Check if item exists:
        if self.db[self.mongo_collection].count_documents({id_key: item[id_key]}) == 0:
            self.db[self.mongo_collection].insert_one(item)
            logger.info("Inserted item in database")
        else:
            logger.info("Item already in database")

        return item
