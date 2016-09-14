import praw
import os
from prawoauth2 import PrawOAuth2Server   
     
user_agent = "ASOIAF Named Weapons Spell Checker v0.0.3"
reddit_client = praw.Reddit(user_agent=user_agent)
app_key = os.environ['APP_KEY']
app_secret = os.environ['APP_SECRET']
scopes = ['identity', 'read', 'submit']

oauthserver = PrawOAuth2Server(reddit_client, app_key, app_secret, state=user_agent, scopes=scopes)
oauthserver.start()

tokens = oauthserver.get_access_codes()
print tokens