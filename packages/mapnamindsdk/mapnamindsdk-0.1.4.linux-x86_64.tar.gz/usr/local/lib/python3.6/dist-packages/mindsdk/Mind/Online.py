import json
import urllib

from mindsdk.Mapper import Mapper as mapper
from mindsdk.WS import WS as WS
import mindsdk.Constants as Constants
import cherrypy
from threading import Thread

from mindsdk.Mind.Mind import Mind


class Online(Mind):

    def __init__(self):
        super(Online,self).__init__()

    @staticmethod
    def _startWS():
        cherrypy.quickstart(WS.MindSdkWebService)

    @staticmethod
    def startWS():
        Thread(target=Online._startWS).start()

    @staticmethod
    def callback():
        print("finished!")

    @staticmethod
    def set(key, value):
        WS.MindSdkWebService.set(key=key, value=value)

    @staticmethod
    def add(key, value):
        WS.MindSdkWebService.add(key=key, value=value)

    @staticmethod
    def getResult(key):
        return WS.MindSdkWebService.getResult(key)

    @staticmethod
    def getResultList(key):
        return WS.MindSdkWebService.getList(key)

    @staticmethod
    def getValue(signalNames):
        # super.getValue(signalName)

        # super(Online).getValue(signalName)
        return super(Online,Online).getValue(signalNames)

    # def createSignal(signalName):
    #     # Create Signal with FALSE Historical Tag
    #     super(Online,Online).createSignal(signalName, False)

    def setValue(signalName, value, dateAndTime, userId):
        super(Online,Online).setValue(signalName, value, dateAndTime, userId)
