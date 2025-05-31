import pytest
from dotenv import load_dotenv
import os
import logging

from dnacentersdk import DNACenterAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

@pytest.fixture
def dna_api():
    # Initialize DNACenterAPI with environment variables
    base_url = os.getenv("DNA_CENTER_BASE_URL")
    username = os.getenv("DNA_CENTER_USERNAME")
    password = os.getenv("DNA_CENTER_PASSWORD")
    version = os.getenv("DNA_CENTER_VERSION", "2.3.7.9")
    verify = os.getenv("DNA_CENTER_VERIFY", "False").lower() == "true"
    logger.info(f"Initializing DNACenterAPI with base_url={base_url}, username={username}, version={version}, verify={verify}")
    return DNACenterAPI(
        base_url=base_url,
        username=username,
        password=password,
        version=version,
        verify=verify
    )

def test_dna_api_object_creation(dna_api):
    logger.info("Testing DNACenterAPI object creation.")
    assert dna_api is not None

def test_get_device_count(dna_api):
    logger.info("Testing get_device_count API call.")
    result = dna_api.devices.get_device_count()
    logger.info(f"Device count API result: {result}")
    assert isinstance(result, dict)
    assert "response" in result
    assert isinstance(result["response"], int)
    assert result["response"] >= 0

def test_get_device_list(dna_api):
    logger.info("Testing get_device_list API call.")
    result = dna_api.devices.get_device_list()
    logger.info(f"Device list API result: {result}")
    assert isinstance(result, dict)
    assert "response" in result
    assert isinstance(result["response"], list)

def test_get_sites_list(dna_api):
    logger.info("Testing get_sites_list API call.")
    result = dna_api.sites.get_site()
    logger.info(f"Site list API result: {result}")
    assert isinstance(result, dict)
    assert "response" in result
    assert isinstance(result["response"], list)

def test_get_topology_vlan_details(dna_api):
    logger.info("Testing get_vlan_details API call by first retrieving a VLAN ID from a device.")
    # Get the list of devices
    devices = dna_api.devices.get_device_list()
    assert "response" in devices and len(devices["response"]) > 0, "No devices found to extract VLAN ID."
    device_id = devices["response"][0]["id"]

    # Get device details
    device_details = dna_api.devices.get_device_by_id(id=device_id)
    logger.info(f"Device details: {device_details}")

    # Attempt to extract a VLAN ID from device details
    vlan_id = None
    # Try common locations for VLAN info
    if "vlanId" in device_details.get("response", {}):
        vlan_id = device_details["response"]["vlanId"]
    elif "vlans" in device_details.get("response", {}):
        vlans = device_details["response"]["vlans"]
        if isinstance(vlans, list) and vlans:
            vlan_id = vlans[0].get("vlanId")
    # Fallback: use a common VLAN ID if not found
    if not vlan_id:
        vlan_id = 1

    logger.info(f"Using VLAN ID: {vlan_id} for topology test.")
    result = dna_api.topology.get_vlan_details(vlan_id=vlan_id)
    logger.info(f"Topology VLAN details API result: {result}")
    assert isinstance(result, dict)
    assert "response" in result

def test_get_all_device_health(dna_api):
    logger.info("Testing get_overall_network_health API call.")
    result = dna_api.health_and_performance.system_health()
    logger.info(f"Overall network health API result: {result}")
    assert isinstance(result, dict)
    assert "healthEvents" in result

    # Optionally, print health for each event if available
    if "healthEvents" in result and isinstance(result["healthEvents"], list):
        for event in result["healthEvents"]:
            logger.info(f"Health Event: {event}")
            