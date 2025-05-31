import subprocess
import time
import os
from dotenv import load_dotenv

load_dotenv()

def connect_vpn():
    print("Connecting to VPN...")
    
    # Path to the Cisco AnyConnect VPN client executable
    vpn_path = r"C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpncli.exe"
    vpn_host = os.getenv("VPN_HOST", "vpn.example.com")  # Default VPN host if not set in .env. Replace with your VPN host.
    username = os.getenv("VPN_USER") # Default username if not set in .env. Replace with your VPN username.
    password = os.getenv("VPN_PASSWORD") # Default password if not set in .env. Replace with your VPN password.

    # Check if the VPN client executable exists
    if not os.path.exists(vpn_path):
        raise FileNotFoundError(f"VPN executable not found at {vpn_path}")
    
    # Ensure that VPN credentials are set
    if not vpn_host or not username or not password:
        raise ValueError("VPN_HOST, VPN_USER, and VPN_PASSWORD must be set in the .env file")
    
    # Start the VPN client process
    # Use subprocess to run the VPN client and pass credentials
    # Note: This assumes the VPN client supports command line interaction for connection
    # Adjust the command as necessary based on your VPN client's requirements
    print(f"Connecting to VPN host: {vpn_host} with user: {username}")

    process = subprocess.Popen(
        [vpn_path, "connect", vpn_host],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    time.sleep(2)
    process.stdin.write(username + "\n")
    process.stdin.flush()
    time.sleep(2)
    process.stdin.write(password + "\n")
    process.stdin.flush()

    stdout, stderr = process.communicate(timeout=30)
    print(stdout)
    print("VPN connected successfully.")
    if stderr:
        print("Error:", stderr)

def disconnect_vpn():
    print("Disconnecting from VPN...")

    # Path to the Cisco AnyConnect VPN client CLI executable
    vpncli_path = r"C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpncli.exe"
    if not os.path.exists(vpncli_path):
        raise FileNotFoundError(f"VPN CLI executable not found at {vpncli_path}")

    # Disconnect the VPN using the CLI
    # Use subprocess to run the VPN client CLI command
    # Adjust the command as necessary based on your VPN client's requirements
    print("Executing VPN disconnect command...")
    process = subprocess.Popen(
        [vpncli_path, "disconnect"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(timeout=15)
    print(stdout)
    print("VPN disconnected successfully.")
    if stderr:
        print("Error:", stderr)