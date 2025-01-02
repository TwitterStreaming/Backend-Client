from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.get_all_tweets_view, name='get_all_tweets'),
    path('search/', views.search_tweets_view, name='search_tweets'), 
    path('trends/', views.trend_view, name='trends'), 
    path('sentiment/', views.sentiment_analysis_view, name='sentiment_analysis'), 
    path('hashtag_count/', views.tweets_per_hashtag_view, name='tweets_per_hashtag'),
    path('tweets/hashtag/', views.get_tweets_by_hashtag_view, name='get_tweets_by_hashtag'),
    path("most-used-hashtag/",views.most_used_hashtag_view, name="most_used_hashtag"),
    path('doc_count/', views.get_doc_count_view, name='get_doc_count'),
]