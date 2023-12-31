import json
from elasticsearch import Elasticsearch
from pymongo import MongoClient

es = Elasticsearch('34.64.147.118:9200')

es.indices.create(
    index='media3',
    settings={
        "analysis": {
            "analyzer": {
                "my_analyzer": {
                    "type": "custom",
                    "tokenizer": "nori_tokenizer"
                }
            }
        }
    },
    mappings={
        "properties": {
            "id": {
                "type": "keyword"
            },
            "title": {
                "type": "text",
                "analyzer": "my_analyzer"
            },
        }
    }
)

client = MongoClient('mongodb://final:123@34.22.93.125:27017/')
db = client['final']
collection = db['movies2']


body = ""
for x in collection.find():
    id = str(x['_id'])
    title = x['title_kr']
    body += json.dumps({"index": {"_index": "media3"}}) + "\n"
    body += json.dumps({"id": id, "title": title}, ensure_ascii=False) + "\n"

es.bulk(body)


   