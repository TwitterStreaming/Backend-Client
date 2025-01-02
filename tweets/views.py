from django.shortcuts import render
from django.http import JsonResponse
from .elasticsearch_client import get_all_tweets
from .elasticsearch_client import search_tweets_by_text
from .elasticsearch_client import get_tweets_trend
from .elasticsearch_client import get_average_sentiment
from .elasticsearch_client import get_tweet_count_by_hashtag
from .elasticsearch_client import get_tweets_by_hashtag
from .elasticsearch_client import get_most_used_hashtag
from .elasticsearch_client import get_doc_count

def get_all_tweets_view(request):
    total_count, tweets = get_all_tweets()
    return JsonResponse({"total": total_count, "tweets": tweets}, safe=False)

def search_tweets_view(request):
    query = request.GET.get('q', '') 
    if not query:
        return JsonResponse({"error": "Query parameter 'q' is required"}, status=400)
    
    total_count, tweets = search_tweets_by_text(query)
    return JsonResponse({"total": total_count, "tweets": tweets}, safe=False)



def trend_view(request):
    query = request.GET.get("q", None)
    interval = request.GET.get("interval", "day")

    if not query:
        return JsonResponse({"error": "Query parameter 'q' is required."}, status=400)

    try:
        trends = get_tweets_trend(query=query, interval=interval)
        return JsonResponse({"trends": trends}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def sentiment_analysis_view(request):
    query = request.GET.get("q", None)

    if not query:
        return JsonResponse({"error": "Query parameter 'q' is required."}, status=400)

    try:
        avg_sentiment = get_average_sentiment(query=query)
        return JsonResponse({"average_sentiment": avg_sentiment}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def tweets_per_hashtag_view(request):
    hashtag = request.GET.get("q", None)

    if not hashtag:
        return JsonResponse({"error": "Query parameter 'q' (hashtag) is required."}, status=400)

    try:
        tweet_count = get_tweet_count_by_hashtag(hashtag)
        return JsonResponse({"hashtag": hashtag, "tweet_count": tweet_count}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)    
    

def get_tweets_by_hashtag_view(request):
    hashtag = request.GET.get("hashtag", None)

    if not hashtag:
        return JsonResponse({"error": "Query parameter 'hashtag' is required."}, status=400)

    try:
        total_count, tweets = get_tweets_by_hashtag(hashtag)
        tweet_data = [{"text": tweet["_source"]["text"], "created_at": tweet["_source"]["created_at"], "hashtags": tweet["_source"]["hashtags"]} for tweet in tweets]
        return JsonResponse({"total_count": total_count, "tweets": tweet_data}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def most_used_hashtag_view(request):
    try:
        most_used_hashtag = get_most_used_hashtag()
        return JsonResponse(most_used_hashtag, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_doc_count_view(request):
    total_count = get_doc_count()
    return JsonResponse({"total_count": total_count})
