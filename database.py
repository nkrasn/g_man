import pymongo
import bot_info

mongo_client = pymongo.MongoClient(bot_info.data['mongo_url'])
gman_db = mongo_client['gman']
inv = gman_db['inventory']
vids = gman_db['videos']
