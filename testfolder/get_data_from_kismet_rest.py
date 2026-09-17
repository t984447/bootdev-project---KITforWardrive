from kismet_rest import Datasources, Devices
from constants import *

### https://github.com/kismetwireless/python-kismet-rest


# Replace with your Kismet host and an API key (admin role for control)
ds = Datasources(host_uri=HOST, apikey=TOKENADMIN, debug=True)
#ds.set_apikey(TOKENADMIN)

print(f"{HOST} and {TOKENADMIN}")
print(f"::: {ds.apikey}")
# (host_uri="http://127.0.0.1:2501", apikey="YOUR_ADMIN_API_KEY")

print(list(ds.all()))

# List datasources
for src in ds.all():
    print(src["kismet.datasource.uuid"], src["kismet.datasource.name"])
