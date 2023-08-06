import json
import urllib
import pandas as pd

from mindsdk.Mapper import Mapper as mapper
from mindsdk.WS import WS as WS
import mindsdk.Constants as Constants
import cherrypy
from threading import Thread

from mindsdk.Mind.Mind import Mind


class Offline(Mind):


    def getUdsValue(signalNames, startDate, endDate):
        pass

    def getValue(signalNames, startDate, endDate, aggregation, interval, pageNumber=1, pageSize=10000):
        try:
            f = mapper.Mapper.getInstance()

            # Get signalId for given signalName from the Mapper
            signalIDs = list(map(lambda x: int(f.SignalMapper[x]), signalNames))

            # Request Body
            body = {"ids": signalIDs,
                    "units": [11, 12, 22],
                    "from_date": startDate,
                    "to_date": endDate,
                    "agg": aggregation,
                    "interval": interval,
                    "page_size": pageSize,
                    "page_number": pageNumber
                    }

            targetUrl = "http://" + Constants.DATASERVICE_SERVER_IP + ":" + Constants.DATASERVICE_PORT + "/historian/get-historian-data"

            req = urllib.request.Request(targetUrl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')

            json_data = json.dumps(body)
            jsonDataAsBytes = json_data.encode('utf-8')  # needs to be bytes
            req.add_header('Content-Length', len(jsonDataAsBytes))

            response = urllib.request.urlopen(req, jsonDataAsBytes)

            jsonResult = response.read()

            # Convert LIST to pandas DataFrame object
            df_result = Offline.convertJsonToDataFrame(jsonResult, signalNames)

            return df_result
        except urllib.error.HTTPError as err:
            print("{}\nError Code:{}, URL:{}".format(err, err.code, err.filename))
        except KeyError as err:
            print("ERROR: Signal Name {} not found!\n".format(err))
        return None


    def getLastValue(signalNames):
        return super(Offline, Offline).getValue(signalNames)

    def setValue(signalName, value, dateAndTime, userId):
        # Insert into online table
        super(Offline, Offline).setValue(signalName, value, dateAndTime, userId)

        '''
        Insert data into Offline table
        '''

        pass
