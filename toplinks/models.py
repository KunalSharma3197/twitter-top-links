from django.db import models
import tables

# Create your models here.
# Model for storing the current user
class User(models.Model) :
    user_id = models.CharField(max_length = 50)
    user_tweet = models.CharField(max_length = 255)

# Model for storing the data of friends of a user
class Friend(models.Model) :
    friend_id = models.CharField(max_length = 50)
    friend_name = models.CharField(max_length = 50)
    friend_screen_name = models.CharField(max_length = 50)
    friend_location = models.CharField(max_length = 50)
    friend_followers_count = models.CharField(max_length = 100)
    friend_friend_count = models.CharField(max_length = 100)
    friend_listed_count = models.CharField(max_length = 100)
    friend_favourite_count = models.CharField(max_length = 100)

# Model for storing tweets
class Tweet(models.Model) :
    tweet_id = models.CharField(max_length = 50)
    tweet_data = models.CharField(max_length = 100)
    tweet_hashtag = models.CharField(max_length = 100)
    tweet_user_id = models.CharField(max_length = 100)
    tweet_user_name = models.CharField(max_length = 100)
    