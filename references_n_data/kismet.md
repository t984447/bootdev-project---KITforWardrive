# Information about and from Kistmet
All responses can be recived as JSON

## API
https://www.kismetwireless.net/docs/api/rest_like/

### Interessting views
https://www.kismetwireless.net/docs/api/device_views/

#### /devices/views/all_views.json
Will show total of found devices for relevant catergory

``
    {
        "kismet.devices.view.id": "phydot11_accesspoints",
        "kismet.devices.view.description": "IEEE802.11 Access Points",
        "kismet.devices.view.size": 23,
        "kismet.devices.view.indexed": 1
    }, 
``

#### /devices/views/phydot11_accesspoints/devices.json
Will show all found devices with ALLOT of data.

