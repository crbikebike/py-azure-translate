__author__ = 'chris'

from CallAzureTranslate import get_translation,init_token
import xmltodict

inputfile = 'inputfiles/AutoOrder.es-MX.resx'
outputfile = 'outputfiles/AutoOrder.es-MX.resx'

#This doc's XML format will either have a string for a value or not - so we want to return that value or None
def get_trans_string(translatedresponse):
    dict_trans = xmltodict.parse(translatedresponse)
    try:
        just_string = dict_trans['string']['#text']
        return (just_string)
    except KeyError:
        return None
    except Exception as e:
        print ("Could not get string value because {}".format(e))

if __name__ == '__main__':

    #initialize the token for Azure
    translate_token = init_token()

    #Open file and load the XML doc into a Dict
    with open(inputfile,mode='r') as fd:
        obj = xmltodict.parse(fd.read())
        #pprint(obj['root']['data'])

    #Translate the string values in the Data elements
    for item in obj['root']['data']:
        translateme = item['value']
        translatedrepsonse = get_translation(text=translateme,azure_token=translate_token)
        translatedstring = get_trans_string(translatedrepsonse)
        if translatedstring is not None:
            print ('{} turned into {}'.format(translateme,translatedstring))
            item['value'] = translatedstring
        else:
            print ('addding None as value')
            item['value'] = None

    #pprint(obj)

    #Go from our updated dict back to XML and write to a file
    with open(outputfile, mode='w') as fd:
        xmlobj = xmltodict.unparse(obj,pretty=True)
        fd.write(xmlobj)