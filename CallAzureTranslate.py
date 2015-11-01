
import requests
import json
from requests.auth import AuthBase
from pprint import pprint

#extend the auth class in requests to make sure the headers match what Azure expects
class AzureAuth(AuthBase):
    """Gives ability to auth with Azure using the Authentication header"""
    def __init__(self,username):
        self.username = username

    def __call__(self,r):
        #return the correct authentication header
        r.headers['Authorization'] = self.username
        return r

#get token for auth to Azure - expires every 10 minutes
def get_access_token():
    try:
        client_id = 'XByjdhZJAnzf2Vqm'
        client_secret = 'kswZypvk/W3TcfaWrEjgC0gl+eSmvWR0QuRUvmd0fmY='
        scope = 'http://api.microsofttranslator.com'
        grant_type = 'client_credentials'
        url = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
        data = {'client_id':client_id,'client_secret':client_secret,'scope':scope,'grant_type':grant_type}
        r = requests.post(url,data)
        rtext = json.loads(r.text)
        return rtext['access_token']
    except Exception as e:
        print ('Could not generate translation key because {}'.format(e))

#Getting a new access token each time because they expire and I'm not sure how to do a timer based on expiration time
def get_translation(text):
    try:
        accesstoken = get_access_token()
        url = 'http://api.microsofttranslator.com/v2/Http.svc/Translate'
        payload = {'text':text,'to':'es','from':'en'}
        auth = 'Bearer {}'.format(accesstoken)
        #print (auth)
        r = requests.get(url=url,params=payload,auth=AzureAuth(auth))
        return r.text

    except Exception as e:
        print ('could not translate because {}'.format(e))

