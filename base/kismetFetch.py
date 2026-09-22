import logging
from datetime import datetime
import configparser
import time
from kismet_rest import Datasources, Devices, BaseInterface, GPS, Messages
#from base.base_interface import BaseInterface

kitLogger = logging.getLogger(__name__)

class tomtenViews(BaseInterface):
    """Get short data from the viewws over the collecting devices"""

    def getNumOfSeen(self) -> dict[str, int]:
        """Return a dict[str, int] wich contains each type and their seen devices From Views: /devices/views/all_views.json"""
        seenData = {}
        url = f"devices/views/all_views.json"
        collectedViews = self.interact("POST", url)
        for dView in collectedViews:
            if (dView["kismet.devices.view.id"] == "phydot11_accesspoints"):
                seenData["WifiAccessPoint"] = (dView["kismet.devices.view.size"])
            elif (dView["kismet.devices.view.id"] == "phy-Bluetooth"):
                seenData["Bluetooth"] = (dView["kismet.devices.view.size"])

        return seenData
    


class kistmetDataFetch:
    """ Big class to collect all the fetching of data from kismet in any way. While heavily based on kismet-rest code there is my own 
    class, tomtenViews, for collecting data otherwise not avaiable via kistmet-rest"""
    def __init__(self, kitsettings: configparser.ConfigParser) -> None:
        self.__hostUrl = kitsettings["kismethost"]["hosturl"]
        self.__loglevel = False
        if (kitsettings["kitsettings"]["loglevel"]) == "DEBUG": self.__loglevel = True
        self.__kismetToken = kitsettings["kismethost"]["apitoken"]
        self.__maxRowDevice = -abs(kitsettings.getint("feeds","maxrowdevice"))
        self.__maxRowMessage = -abs(kitsettings.getint("feeds","maxrowmessage"))

        # Objects based on kimet-rest to fetch various data
        self.__kismetDS = Datasources(host_uri=self.__hostUrl, apikey=self.__kismetToken, debug=self.__loglevel)
        self.__kismetDEV = Devices(host_uri=self.__hostUrl, apikey=self.__kismetToken, debug=self.__loglevel)
        self.__kismetViews = tomtenViews(host_uri=self.__hostUrl, apikey=self.__kismetToken, debug=self.__loglevel)
        self.__kismetGPS = GPS(host_uri=self.__hostUrl, apikey=self.__kismetToken, debug=self.__loglevel)
        self.__kismetMessages = Messages(host_uri=self.__hostUrl, apikey=self.__kismetToken, debug=self.__loglevel)

    def printDataSources(self) -> None:
        """Print all current collecting devices, sources so to speak."""
        for src in self.__kismetDS.all():
            print(f"""
            UUID: {src["kismet.datasource.uuid"]}
            Name: {src["kismet.datasource.name"]}
            Packets captured: {src["kismet.datasource.num_packets"]}
            """)
            print("----------")
        pass

    def listDataSources(self) -> list[tuple()]:
        """ returns all current collecting devices, sources so to speak"""
        dataSourcesList = []
        for dsrc in self.__kismetDS.all():
            dataSourcesList.append((dsrc["kismet.datasource.uuid"], dsrc["kismet.datasource.name"], dsrc["kismet.datasource.num_packets"]))
        return dataSourcesList


    def printDataSourcesSeen(self) -> None:
        """ Prints stats from the collecting sources of Wifi access points and Bluetooth """
        collectedViews = self.__kismetViews.getNumOfSeen()
        for view in collectedViews:
            print(f"{view} has seen {collectedViews[view]}")
        pass

    def getDataSourcesSeen(self) -> dict[str, int]:
        """ Returns a dict with stats from the collecting sources of Wifi access points and Bluetooth """
        return self.__kismetViews.getNumOfSeen()


    def printWifiDevicesXSeconds(self, mSeconds: int=10) -> None:
        """ Fetches all devices last modified within mSeconds ago. Prints Device, common-name and signalstrength.
        Provide an INT which represent how many seconds back the list should contain, Default is last 10 seconds """
        for tDev in self.__kismetDEV.dot11_access_points(last_time=(int(time.time()) - mSeconds),fields=['kismet.device.base.commonname', 'kismet.device.base.signal', 'kismet.device.base.macaddr', 'kismet.device.base.last_time']):
            if tDev['kismet.device.base.commonname'] == tDev['kismet.device.base.macaddr']: nDev = "Hidden SSID" 
            else: nDev = tDev['kismet.device.base.commonname']
            print("---------")
            print(tDev)
            print("---------")
            print(f"""
            Name: {nDev}
            Signal: {tDev["kismet.device.base.signal"]["kismet.common.signal.last_signal"]}
            Mac: {tDev["kismet.device.base.macaddr"]}
            LastTime: {tDev["kismet.device.base.last_time"]}
            """)
            print("---------")
            break

    def listWifiDevicesXSeconds(self, mSeconds: int=10) -> list[tuple()]:
        """ Fetches all devices last modified within mSeconds ago. Returns list[tuple] with Device, common-name and signalstrength
        Provide an INT which represent how many seconds back the list should contain, Default is last 10 seconds  """
        deviceList = []
        for dsrc in self.__kismetDEV.dot11_access_points(last_time=(int(time.time()) - mSeconds),fields=['kismet.device.base.commonname', 'kismet.device.base.signal', 'kismet.device.base.macaddr', "kismet.device.base.last_time"]):
            if dsrc['kismet.device.base.commonname'] == dsrc['kismet.device.base.macaddr']: nDev = "Hidden SSID" 
            else: nDev = dsrc['kismet.device.base.commonname']
            deviceList.append((nDev, (dsrc["kismet.device.base.signal"]["kismet.common.signal.last_signal"]), (dsrc["kismet.device.base.macaddr"]), (datetime.fromtimestamp(dsrc["kismet.device.base.last_time"]).strftime("%H:%M:%S"))))
        deviceList.sort(key=lambda tup: tup[3])
        return deviceList[self.__maxRowDevice:]

    def listGPSstats(self):
        return self.__kismetGPS.current_location()

    def listMessages(self, tsSeconds: int=1, msSeconds: int=0, ammount: int = 10) -> list[tuple()]:
        """ Fetches all messages since (tsSeconds).(msSeconds) ago. Returns list[tuple] with message and timestamp, sorted by timestanp
        Provide an INT Seconds and uSeconds represent how many seconds back the list should contain, Default is last 1.0 seconds  """
        fetchedMessages = self.__kismetMessages.all(ts_sec=tsSeconds, ts_usec=msSeconds)
        messageList = []
        for message in fetchedMessages:
            kitLogger.debug(f"Fetched messages, found {len(message["kismet.messagebus.list"])}")
            for mess in message["kismet.messagebus.list"]:
                messageList.append(((mess["kismet.messagebus.message_string"]), (datetime.fromtimestamp(mess["kismet.messagebus.message_time"]).strftime("%H:%M:%S"))))
                
        messageList.sort(key=lambda tup: tup[1])
        return messageList[self.__maxRowMessage:]

    def quickListMessages(self, tsSeconds: int=1, msSeconds: int=0):
        return self.__kismetMessages.all(ts_sec=tsSeconds, ts_usec=msSeconds)