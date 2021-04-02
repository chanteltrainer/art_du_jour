#!/usr/bin/env python

import tweepy


def authorize_user():
    secrets = get_secrets()

    #for developer account
    CONSUMER_KEY = secrets['consumer key']
    CONSUMER_SECRET = secrets['consumer secret']

    print(f'{CONSUMER_KEY} {CONSUMER_SECRET}')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.secure = True
    auth_url = auth.get_authorization_url()

    print ('Please authorize: ' + auth_url)

    verifier = input('PIN: ').strip()

    auth.get_access_token(verifier)

    #prints out access key for authorized user account
    print ("ACCESS_KEY = '%s'" % auth.access_token)
    print ("ACCESS_SECRET = '%s'" % auth.access_token_secret)


def get_secrets():
    secrets = {}
    with open('twitter.secrets') as f:
        lines = f.readlines()
        secrets['consumer key'] = lines[0].split(':')[1].strip()
        secrets['consumer secret'] = lines[1].split(':')[1].strip()
        secrets['access key'] = lines[2].split(':')[1].strip()
        secrets['access secret'] = lines[3].split(':')[1].strip()
    return secrets
        