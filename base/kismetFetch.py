import logging
#import kismet_rest
import time
from kismet_rest import Datasources, Devices, BaseInterface
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
    def __init__(self, hostUrl: str = "http://127.0.01:2501", kismetToken: str = "xxxxxxxxx", loglevel = "INFO") -> None:
        self.__hostUrl = hostUrl
        self.__loglevel = False
        if loglevel == "DEBUG": self.__loglevel = True
        self.__kismetToken = kismetToken
        self.__kismetDS = Datasources(host_uri=self.__hostUrl, apikey=self.__kismetToken, debug=self.__loglevel)
        self.__kismetDEV = Devices(host_uri=self.__hostUrl, apikey=self.__kismetToken, debug=self.__loglevel)
        self.__kismetViews = tomtenViews(host_uri=self.__hostUrl, apikey=self.__kismetToken, debug=self.__loglevel)

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
            deviceList.append((nDev, (dsrc["kismet.device.base.signal"]["kismet.common.signal.last_signal"]), (dsrc["kismet.device.base.macaddr"]), dsrc["kismet.device.base.last_time"]))
        deviceList.sort(key=lambda tup: tup[3])
        return deviceList