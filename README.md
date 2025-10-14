# IP Analyzer

## Overview
This project is a **Python-based prototype** to quickly retrieve and display their computer’s **public IPv4 and IPv6 addresses**.

In addition to IP information, the application provides **geolocation**, **ISP**, and **ASN (Autonomous System Number)** data using **public REST APIs**.

The tool serves as a foundation for future enhancements such as GUI visualization, IP change monitoring, or network diagnostics.

---

## Features

- Retrieves **both IPv4 and IPv6** addresses  
- Displays **geolocation** (City, Region, Country, Coordinates)  
- Shows **ISP** and **ASN** information  
- Displays **timezone** based on IP location  
- Includes **error handling** for API failures or connection issues  
- Presents data in a **clean, unified output**

---

## Technologies Used

| Component | Purpose |
|------------|----------|
| **Python 3** | Core programming language |
| **Requests Library** | For making REST API calls |
| **ipify API** | To get current public IPv4 and IPv6 addresses |
| **ipinfo.io API** | To retrieve geolocation, ISP, and ASN information |

---

## Project Architecture

