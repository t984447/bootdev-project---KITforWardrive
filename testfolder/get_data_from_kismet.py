import requests
from constants import *

#url = f"{HOST}/devices/views/all_views.json"
url = f"{HOST}/datasource/all_sources.itjson"

response = requests.get(
    url,
    cookies={
        "KISMET": TOKEN
    }
)

response.raise_for_status()
data = response.json()
#print(data)


#from pprint import pprint

#pprint(data)

#for device in data:
#    print(device["kismet.devices.view.id"])
#    print(device["kismet.devices.view.size"])

for uuid in data:
    print(uuid["kismet.devices.view.id"])
    print(uuid["kismet.devices.view.size"])


class KismetData():
    def __init__(self, token: STR, hosturl: STR) -> None:
        self.__token = token
        self.__data = None
        self.host = hosturl
        self.devURL = f"{HOST}/devices/views/all_views.json"

    def UpdateDevice() -> None:
        pass

    def UpdateMetaData() -> None:
        pass

    def PrintMetatotal() -> None:
        pass