# Headless Setup for Raspberry Pi

Process to setup a Raspberry Pi to run in headless mode - no keyboard and monitor - by enabling SSH and configuring the Wifi. 
First create the SD Card with the Raspberry Pi OS (formerly known as Raspbian) image. Insert it into an SD Reader to access
the partition labelled as `boot` on the card.

## Enable SSH
Create an empty file named `ssh` in the boot partition.

## Setting up WiFi
Create a file named `wpa_supplicant.conf` in the boot partition and add this
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert 2 letter ISO 3166-1 country code here>

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}
```

## Get the IP Address of the Raspberry PI
* Using nmap scan the local network
  ```bash
  $ nmap -sn 192.168.10.0/24
  ```
  Look for the device with hostname `raspberrypi`

* Using mDNS, try to resolve `raspberrypi.local`
  ```bash
  $ ping raspberrypi.local
  ```

---
Source: [https://www.raspberrypi.org/documentation/configuration/wireless/headless.md](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)
