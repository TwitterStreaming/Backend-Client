from elasticsearch import Elasticsearch
from django.conf import settings

es_client = Elasticsearch(
    [settings.ES_HOST],
    http_auth=settings.ES_AUTH,
    verify_certs=False
)

def get_all_tweets():
    body = {
        "query": {"match_all": {}},
        "size": 1000
    }
    response = es_client.search(index="streaming", body=body)
    return response["hits"]["total"]["value"], response["hits"]["hits"]

def search_tweets_by_text(query):
    body = {
        "query": {"match": {"text": query}},
        "size": 9999
    }
    response = es_client.search(index="streaming", body=body)
    return response["hits"]["total"]["value"], response["hits"]["hits"]

def get_tweets_trend(query, interval):
    body = {
            "size": 0,
            "query": {
                "match": {
                    "text": query,
                    }
                },
            "aggs": {
                "tweets_over_time": {
                    "date_histogram": {
                        "field": "created_at",
                        "fixed_interval": interval,
                        "format": "yyyy-MM-dd HH:MM:SS",
                        "time_zone": "UTC",
                        "min_doc_count": 1
                        }
                    }
                }
    }

    response = es_client.search(index="streaming", body=body)
    return [
        {"date": bucket["key_as_string"], "count": bucket["doc_count"]}
        for bucket in response["aggregations"]["tweets_over_time"]["buckets"]
    ]

def get_average_sentiment(query):
    body = {
        "query": {"match": {"text": query}},
        "aggs": {
            "nested_sentiment": {
                "nested": {"path": "sentiment"},
                "aggs": {
                    "average_polarity": {"avg": {"field": "sentiment.polarity"}},
                    "average_subjectivity": {"avg": {"field": "sentiment.subjectivity"}}
                }
            }
        },
        "size": 0
    }
    response = es_client.search(index="streaming", body=body)
    nested_sentiment = response["aggregations"]["nested_sentiment"]
    return {
        "average_polarity": nested_sentiment["average_polarity"]["value"],
        "average_subjectivity": nested_sentiment["average_subjectivity"]["value"]
    }

def get_tweet_count_by_hashtag(hashtag):
    body = {
        "query": {"match": {"hashtags": hashtag}},
        "size": 0
    }
    response = es_client.search(index="streaming", body=body)
    return response["hits"]["total"]["value"]

def get_tweets_by_hashtag(hashtag):
    body = {
        "query": {"match": {"hashtags": hashtag}},
        "size": 1000
    }
    response = es_client.search(index="streaming", body=body)
    return response["hits"]["total"]["value"], response["hits"]["hits"]

def get_most_used_hashtag():
    body = {
        "size": 0,
        "aggs": {
            "most_used_hashtag": {
                "terms": {
                    "field": "hashtags.keyword", 
                    "size": 1 
                }
            }
        }
    }

    response = es_client.search(index="streaming", body=body)
    buckets = response["aggregations"]["most_used_hashtag"]["buckets"]

    if buckets:
        return {"hashtag": buckets[0]["key"], "count": buckets[0]["doc_count"]}
    return {"hashtag": None, "count": 0}
