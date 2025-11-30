"""
IP Analyzer Application
-----------------------------------------
This program retrieves a computer's public IPv4 and IPv6 addresses
and provides additional network details such as ISP, ASN, and location.

APIs Used:
1. ipify.org  - for retrieving the current public IP addresses (IPv4 & IPv6)
2. ipinfo.io  - for retrieving geolocation, ISP, and ASN information

Author: NovaTech
Version: 1.0
"""

import requests

def get_ip(version="ipv4"):
    """
    Retrieves the public IP address for the specified version (IPv4 or IPv6).
    
    Parameters:
        version (str): The IP version to retrieve ("ipv4" or "ipv6").
    
    Returns:
        str: The public IP address or an error message if retrieval fails.
    """
    try:
        if version == "ipv6":
            url = "https://api64.ipify.org?format=json"
        else:
             url = "https://api.ipify.org?format=json"

        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json().get("ip")
    
    except Exception as e:
        return f"Error fetching {version}: {e}"

def get_ip_info():
    """
    Retrieves geolocation and ISP information for a given IP address
    using the ipinfo.io public API.
    
    Parameters:
        ip (str): The IP address to look up.
    
    Returns:
        dict A dictionary containing location, ISP, ASN, and timezone information.
    """
    try:
        response = requests.get("https://ipapi.co/json/", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    """
    Main function that controls the flow of the application.
    Retrieves both IPv4 and IPv6 addresses, fetches location/ISP info,
    and displays all details in a formatted output.
    """
    print("\n--- IP Analyzer ---")

    # Get both IPv4 and IPv6
    ipv4 = get_ip("ipv4")
    ipv6 = get_ip("ipv6")

    # Get additional information from ipapi
    info = get_ip_info()

    if "error" in info:
        print(f"Could not fetch details: {info['error']}")
        return

    # Display results in one block
    print(f"IPv4 Address: {ipv4}")
    print(f"IPv6 Address: {ipv6}")
    print(f"City: {info.get('city', 'N/A')}")
    print(f"Region: {info.get('region', 'N/A')}")
    print(f"Country: {info.get('country_name', 'N/A')} ({info.get('country_code', 'N/A')})")
    print(f"Latitude, Longitude: {info.get('latitude', 'N/A')}, {info.get('longitude', 'N/A')}")
    print(f"Timezone: {info.get('timezone', 'N/A')}")
    print(f"ISP: {info.get('org', 'N/A')}")
    print(f"ASN: {info.get('asn', 'N/A')}")
    print("-------------------------------------")

if __name__ == "__main__":
    main()
