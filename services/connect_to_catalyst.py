import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv, set_key
from connect_to_vpn import connect_vpn, disconnect_vpn
import urllib3

load_dotenv()

# connect_vpn()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DNAC_URL = os.getenv("DNA_CENTER_BASE_URL")
USERNAME = os.getenv("DNA_CENTER_USERNAME")
PASSWORD = os.getenv("DNA_CENTER_PASSWORD")

def get_auth_token():
    url = f"{DNAC_URL}/dna/system/api/v1/auth/token"
    response = requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
    response.raise_for_status()
    set_key("./.env", "CURR_TOKEN", response.json()["Token"])
    return response.json()["Token"]

if __name__ == "__main__":
    token = get_auth_token()
    print("Connected to Catalyst")
    # disconnect_vpn()