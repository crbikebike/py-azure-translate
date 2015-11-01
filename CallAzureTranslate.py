
import requests
import json
from requests.auth import AuthBase
from datetime import datetime,timedelta
from azureconf import azureconf


azure_client_id = azureconf['client_id']
azure_client_secret = azureconf['client_secret']
azure_token = None


#extend the auth class in requests to make sure the headers match what Azure expects
class AzureAuth(AuthBase):
    """Gives ability to auth with Azure using the Authentication header"""
    def __init__(self,username):
        self.username = username

    def __call__(self,r):
        #return the correct authentication header
        r.headers['Authorization'] = self.username
        return r


class TranslateToken(object):
    def __init__(self,client_id,client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        #get token for auth to Azure - expires every 600 seconds
        try:
            request_time = datetime.now()
            scope = 'http://api.microsofttranslator.com'
            grant_type = 'client_credentials'
            url = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
            data = {'client_id':self.client_id,'client_secret':self.client_secret,'scope':scope,'grant_type':grant_type}
            r = requests.post(url,data)
            rtext = json.loads(r.text)
            #Take expire time and minus a minute to be safe
            expires_in = (int(rtext['expires_in']) - 60)
            expire_delta = timedelta(seconds=expires_in)

            #token info to be referenced by calling functions
            self.access_token = rtext['access_token']
            self.expiretime = request_time + expire_delta
        except Exception as e:
            print ('Could not generate translation key because {}'.format(e))

def init_token():
    azure_init = TranslateToken(client_id=azure_client_id,client_secret=azure_client_secret)
    return azure_init

#If token's end time is still valid, return original token, if not, or is None, init a new one and return that
def check_token(token):
    global azure_token
    try:
        if token is None or token.expiretime <= datetime.now():
            azure_token = init_token()
            token = azure_token
            return token
        elif token.expiretime > datetime.now():
            return  token
        else:
            raise Exception
    except Exception as e:
        print ("Did not check token because {}".format(e))

#Takes in a string, then returns the response from Azure Translate
def get_translation(text):
    global azure_token
    #make sure the token passed is still valid
    translate_token = check_token(azure_token)
    try:
        accesstoken = translate_token.access_token
        url = 'http://api.microsofttranslator.com/v2/Http.svc/Translate'
        payload = {'text':text,'to':'es','from':'en'}
        auth = 'Bearer {}'.format(accesstoken)
        r = requests.get(url=url,params=payload,auth=AzureAuth(auth))
        return r.text

    except Exception as e:
        print ('could not translate because {}'.format(e))

