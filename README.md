# README #

## Version 1.0 Summary ##

This repo consists of three main files: CallAzureTranslate.py, main.py, and azureconf.py

The three together represent one implementation that ingests an XML file containing key value relationships for a webpages language association files.  The longterm intent is to develop cousins of CallAzureTranslate that would be agnostic to implementation.  

## File Summaries ## 

**azureconf.py**

Simple method for providing client_id and client_secret.  An example is given via the azureconf_example.py.  Replace your secrets as necessary in the file.  Looking for better ways to implement this if anyone has suggestions.

**CallAzureTranslate.py**

An example of the repo's goal, a toolset for hitting Azure with Python.  Azure tokens expire every 10 minutes, so a refresh function will grab a new token if needed.

*Primary Usage*

Contains a function named get_translate that will take an English string and return Spanish string from Azure's Translation service.  Currently hardcoded to go from English to Spanish.  Lots of other config options to be had in the future.

**main.py**

An example of implementing the CallAzureTranslate.py module.  Takes in an XML file and parses each <data> tag to translate its string value from English to Spanish.  Exists as an example and to satisfy an urgent need for a specific project.

## Contact ##

If you have any comments or suggestions, please reach out!  chris at eatingrd dot com