import os

from dotenv import load_dotenv
from pymongo import MongoClient
import VehicleAd

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client['OtomotoParserDB']                             # choose database
collection = db['Advertisement']


def save_ad_to_database(VehicleAd: VehicleAd):
    insert_data = VehicleAd.to_json()
    collection.update_one(
        {"link": insert_data["link"]},  # Match condition
        {"$setOnInsert": insert_data},  # Insert only if not found
        upsert=True
    )


def get_ad_by_link(link: str):
    return collection.find_one({"link": link})

