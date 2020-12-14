from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import oauth2 as oauth
from django.http import HttpResponseServerError
from twitter_top_links.settings import SOCIAL_AUTH_TWITTER_KEY as c_key
from twitter_top_links.settings import SOCIAL_AUTH_TWITTER_SECRET as secret_key
from toplinks.models import Friend
from toplinks.models import User
from toplinks.models import Tweet
# Create your views here.

twitter_exception="<html><body background=#dddddd font-family:sans-serif><h1> Something is not happening!</h1></body></html>"

def call_twitter_api(endpoint):
    oauth_consumer = oauth.Consumer(key=c_key, secret=secret_key)
    oauth_token = oauth.Token(key="1337725078662889474-RoxvhE6tJ1ZPADhQtoBUkNkj6hpyuL", secret="vJF70rjhPXFlBra0OENmY2UtE8lTRGUmU2J5bG6rIY7AZ")
    client = oauth.Client(oauth_consumer, oauth_token)
    response, data = client.request(endpoint)
    return response, json.loads(data)

# Get users timeline 
def get_user_tweets(request) :
    username = request.user
    timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s Tweet&count=20"%(username)
    resp, tweets = call_twitter_api(timeline_endpoint)
    context = {'tweet': tweets}
    if resp.status != 200:
        print("status exception get_user_tweets", resp.status)
        return HttpResponseServerError(twitter_exception)
    else:
        for tweet in tweets :
            try :
                obj =  User.objects.get(user_id = tweet['id'], user_tweet = tweet['text'])
            except User.DoesNotExist :
                obj =  User(user_id = tweet['id'], user_tweet = tweet['text'])
                obj.save()
        print("status working get_user_tweets", resp.status)
        return render(request, 'getusertweet.html', context)

# Get Friends list
def get_friends(request):
    timeline_endpoint = "https://api.twitter.com/1.1/friends/list.json?cursor=-1&screen_name=%s "  \
                        "Tweet&skip_status=true&include_user_entities=false "%(request.user)
    resp, friends_list = call_twitter_api(timeline_endpoint)

    # for friends in friends_list['users']:
    #     print('\nid : ', friends['id'], '\nName : ', friends['name'], '\nScreen Name : ', friends['screen_name'],
    #           '\nLocation : ', friends['location'], '\nFollowers Count : ', friends['followers_count'],
    #           '\nFriends Count : ', friends['friends_count'], '\nListed Count : ', friends['listed_count'],
    #           '\nFavourites Count : ', friends['favourites_count'])

    context = {'friends': friends_list['users']}
    
    if resp.status != 200:
        print("status exception get_friends", resp.status)
        return HttpResponseServerError(twitter_exception)
    else:
        for friends in friends_list['users'] :
            try :
                obj = Friend.objects.get(
                    friend_id = friends['id'],
                    friend_name = friends['name'],
                    friend_screen_name = friends['screen_name'],
                    friend_location = friends['location'],
                    friend_followers_count = friends['followers_count'],
                    friend_friend_count = friends['friends_count'],
                    friend_listed_count = friends['listed_count'],
                    friend_favourite_count = friends['favourites_count']
                )
            except Friend.DoesNotExist :
                obj = Friend(
                    friend_id = friends['id'],
                    friend_name = friends['name'],
                    friend_screen_name = friends['screen_name'],
                    friend_location = friends['location'],
                    friend_followers_count = friends['followers_count'],
                    friend_friend_count = friends['friends_count'],
                    friend_listed_count = friends['listed_count'],
                    friend_favourite_count = friends['favourites_count']
                )
                obj.save()
        print("status working get_friends", resp.status)
        return render(request, 'getfriends.html', context)

# Pulls tweets over last 7 days from user and friends 
def pull_all_tweets(request) :
    timeline_endpoint = "https://api.twitter.com/1.1/statuses/home_timeline.json?screen_name=%s Tweet&count=200"%(request.user)
    resp, tweets = call_twitter_api(timeline_endpoint)
    context = {'tweet': tweets}
    if resp.status != 200:
        print("status exception get_user_tweets", resp.status)
        return HttpResponseServerError(twitter_exception)
    else:
        for tweet in tweets :
            # print(tweet['entities']['hashtags'][0]['text']) 
            # print(tweet['user']['id'])
            # print(tweet['user']['name'])
            try :
                hashtag = ""
                if len(tweet['entities']['hashtags']) > 0 :
                    hashtag = tweet['entities']['hashtags'][0]['text']
                obj = Tweet.objects.get(tweet_id = tweet['id'], tweet_data = tweet['text']
                    , tweet_hashtag = hashtag, tweet_user_id = tweet['user']['id']
                    , tweet_user_name = tweet['user']['name'])
            except Tweet.DoesNotExist :
                obj = Tweet(tweet_id = tweet['id'], tweet_data = tweet['text']
                    , tweet_hashtag = hashtag, tweet_user_id = tweet['user']['id']
                    , tweet_user_name = tweet['user']['name'])
                obj.save()
        print("status working get_user_tweets", resp.status)
        return render(request, 'getalltweets.html', context)
     
# returns a list of current most discussed topics
def get_most_discussed_topic(request) :
    entries = Tweet.objects.values('tweet_hashtag')
    frequency_map = {}
    for entry in entries :
        if len(entry['tweet_hashtag']) > 0 :
            key = entry['tweet_hashtag']
            if key in frequency_map :
                frequency_map[key] += 1
            else :
                frequency_map[key] = 1
    topics = []
    count = 0
    for w in sorted(frequency_map, key=frequency_map.get, reverse=True) :
        if count == 10 :
            break
        topics.append(w)
        count += 1
    print(len(topics))
    context = {'topics' : topics}
    return render(request, 'getmostdiscussedtopic.html', context)

# returns the person with most tweets
def get_person_with_most_tweets(request) :
    entries = Tweet.objects.values('tweet_user_id')
    frequency_map = {}
    map = {}

    for entry in entries :
        if len(entry['tweet_user_id']) > 0 :
            key = entry['tweet_user_id']
            if key in frequency_map :
                frequency_map[key] += 1
            else :
                frequency_map[key] = 1
    user_id = max(frequency_map, key = frequency_map.get)
    querry_set = Tweet.objects.filter(tweet_user_id = user_id).values('tweet_user_name')
    for q in querry_set :
        user_name = q['tweet_user_name']
        break
    context = {'user_name' : user_name}
    # print(context)
    return render(request, 'getpersonwithmosttweets.html', context)
