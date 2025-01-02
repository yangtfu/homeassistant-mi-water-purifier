# homeassistant-mi-water-purifier
XiaoMi Water Purifier component for Home Assistant.

Forked from https://github.com/bit3725/homeassistant-mi-water-purifier.
Rewrite coordinator and sensor platform.

## Installation

1. Add repository to HACS custom repository and search xiaomi water purifier or copy *custom_components/mi_water_purifier* to **.homeassistant/custom_components/**.
2. Get the IP of your sensor.
3. Follow [Retrieving the Access Token](https://home-assistant.io/components/vacuum.xiaomi_miio/#retrieving-the-access-token) guide to get the token of your sensor

## Configuration
```yaml
sensor:
  - platform: mi_water_purifier
    host: YOUR_SENSOR_IP
    token: YOUR_SENSOR_TOKEN
    scan_interval: YOUR_SCAN_INTERVAL
```
