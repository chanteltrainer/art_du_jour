#!/usr/bin/env python

import tweepy

# From your app settings page
CONSUMER_KEY = "XN3fr1J5qiwGa4GDG2X5fvIEz"
CONSUMER_SECRET = "tmGESo2VOXvwmDRhxI6x7QIVYDl6HEBDAkrDFcyq4RHkmUw3x4"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.secure = True
auth_url = auth.get_authorization_url()

print ('Please authorize: ' + auth_url)

verifier = input('PIN: ').strip()

auth.get_access_token(verifier)

print ("ACCESS_KEY = '%s'" % auth.access_token)
print ("ACCESS_SECRET = '%s'" % auth.access_token_secret)