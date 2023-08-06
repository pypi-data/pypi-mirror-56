import urllib.request
import urllib.parse
import json

import mindsdk.Constants as Constants

class Mapper:
    __instance=None

    SignalMapper=None


    @staticmethod
    def getInstance():

        if Mapper.__instance==None:
            Mapper()
        return Mapper.__instance


    @staticmethod
    def getMapper():
        url = 'http://'+Constants.SIGNALSERVICE_SERVER_IP+':'+Constants.SIGNALSERVICE_PORT+'/getmapper'
        f = urllib.request.urlopen(url)
        response = f.read().decode('utf-8')

        dict_response = json.loads(response)
        dict_result = {}
        for signal in dict_response:
            if dict_response[signal]['plantId']==3:
                dict_result[dict_response[signal]['signalName']] = signal

        # pprint(response)
        return dict_result

    def __init__(self):
        """ Virtually private constructor. """
        if Mapper.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Mapper.SignalMapper=Mapper.getMapper()
            Mapper.__instance = self



