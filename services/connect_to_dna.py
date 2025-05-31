from connect_to_vpn import connect_vpn, disconnect_vpn

from dnacentersdk import DNACenterAPI
import urllib3

# connect_vpn()

urllib3.disable_warnings()

api = DNACenterAPI()

print(api.devices.get_device_count())

# disconnect_vpn()
