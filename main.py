__author__ = 'chris'

from CallAzureTranslate import AzureTranslator
import xmltodict
from azureconf import azureconf

azure_client_id = azureconf['client_id']
azure_client_secret = azureconf['client_secret']

inputfile = 'inputfiles/AutoOrder.es-MX.resx'
outputfile = 'outputfiles/AutoOrder.es-MX.resx'

if __name__ == '__main__':

    #define translator object that will do the heavy lifting
    translator = AzureTranslator(azure_client_id, azure_client_secret)

    #Open file and load the XML doc into a Dict
    with open(inputfile,mode='r') as fd:
        obj = xmltodict.parse(fd.read())
        #pprint(obj['root']['data'])

    #Translate the string values in the Data elements
    for item in obj['root']['data']:
        translateme = item['value']
        translatedstring = translator.translate(translateme)
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