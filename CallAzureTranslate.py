
import requests
import json
import xmltodict
from requests.auth import AuthBase
from datetime import datetime,timedelta


#extend the auth class in requests to make sure the headers match what Azure expects
class AzureAuth(AuthBase):
    """Gives ability to auth with Azure using the Authentication header"""
    def __init__(self,access_token):
        self.access_token = access_token

    def __call__(self,r):
        #return the correct authentication header
        r.headers['Authorization'] = self.access_token
        return r

#this is an Azure access token that will expire 10 minutes after creation
class AzureToken(object):
    def __init__(self,access_token, expiry_seconds):
        self.access_token = access_token
        self.expiry_seconds = int(expiry_seconds)
        #Subtract 60 seconds form expire seconds for buffer
        self.expiry_seconds -= 60
        self.expire_time = datetime.now() + timedelta(seconds=self.expiry_seconds)

    def access_token(self):
        return self.access_token

    def is_expired(self):
        return self.expire_time <= datetime.now()

#This is what can be imported and used to get a string from English to Spanish
class AzureTranslator(object):
    def __init__(self,client_id,client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    #method called to translate text
    def translate(self, text):
        response = self.request_translation(text)
        #Azure returns an XML set with lots of extra data, strip all that and return only string or None
        dict_trans = xmltodict.parse(response)
        try:
            just_string = dict_trans['string']['#text']
            return (just_string)
        except KeyError:
            return None
        except Exception as e:
            print ("Could not get string value because {}".format(e))


    def request_translation(self,text):
        #make sure token is still valid
        token = self.get_token()

        #with valid token, call Azure translate service
        try:
            url = 'http://api.microsofttranslator.com/v2/Http.svc/Translate'
            payload = {'text':text,'to':'es','from':'en'}
            auth = 'Bearer {}'.format(token.access_token)
            r = requests.get(url=url,params=payload,auth=AzureAuth(auth))
            return r.text

        except Exception as e:
            print ('could not translate because {}'.format(e))

    #return new or valid token, depending on state of self.token
    def get_token(self):
        try:
            if self.token is None or self.token.is_expired():
                self.refresh_token()
                return self.token
            else:
                return self.token
        except Exception as e:
            print ("Did not get token because {}".format(e))

    #when self.token is expired or None, called to get a valid access token
    def refresh_token(self):
        #grab new auth token when called
        try:
            scope = 'http://api.microsofttranslator.com'
            grant_type = 'client_credentials'
            url = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
            data = {'client_id':self.client_id,'client_secret':self.client_secret,'scope':scope,'grant_type':grant_type}
            r = requests.post(url,data)
            rtext = json.loads(r.text)

            #token info to be referenced by calling functions
            self.access_token = rtext['access_token']
            self.expires_in = rtext['expires_in']
            self.token = AzureToken(self.access_token, self.expires_in)

        except Exception as e:
            print ('Could not generate translation key because {}'.format(e))
