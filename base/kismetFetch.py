import logging
#import kismet_rest
from kismet_rest import Datasources, Devices

kitLogger = logging.getLogger(__name__)

class kistmetDataFetch:
    def __init__(self, hostUrl, kismetToken) -> None:
        self.__kismetDS = Datasources(host_uri=hostUrl, apikey=kismetToken) 

    def printDataSources(self) -> None:
        print(self.__kismetDS)
        for src in self.__kismetDS.all():
            print(src["kismet.datasource.uuid"], src["kismet.datasource.name"])
        pass