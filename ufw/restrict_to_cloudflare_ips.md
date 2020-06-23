# Only Allow Traffic from Cloudflare's IP Addresses

I have some services and apps running on a RaspberryPi on my home network and want to access them even 
when I am not on my network. To do this, first I use CloudFlare to proxy all the traffic to the home.
But I want to block any traffic thats trying to reach the RPi thats not coming from Cloudflare.

* IMPORTANT: Enable ssh access from local network
  ```bash
  $ ufw allow from 192.168.1.0/24 to any port 22 proto tcp comment "Allow SSH from local network" 
  ```
  OR: Allow all traffic from local network if its trusted
  ```bash
  $ ufw allow from 192.168.1.0/24 to any comment "Allow all local LAN traffic"
  ```
* Enable traffic to DCHP server (e.g pi-hole)
  ```
  $ ufw allow from any port 67,68 proto udp
  ```
* Clear any rules that allow traffic on port 80 and 443 from anywhere
  ```bash
  $ ufw status numbered
  $ ufw delete <rule-no>
  ```
* Allow TCP Traffic from Cloudflare's Published IP Addresses.<br>
  `/home/pi/.ufw/cloudflare-ufw.sh`
  ```bash
  #!/bin/sh

  # clear any existing Cloudflare IP rules
  for NUM in $(ufw status numbered | grep 'Cloudflare IP' | awk -F '[][]' '{print $2}' | sort -rn | tr --delete [:blank:])
  do
    ufw --force delete $NUM
  done

  curl -s https://www.cloudflare.com/ips-v4 -o /tmp/cf_ips
  curl -s https://www.cloudflare.com/ips-v6 >> /tmp/cf_ips

  # Allow all traffic from Cloudflare IPs (no ports restriction)
  for cfip in `cat /tmp/cf_ips`; do ufw allow proto tcp from $cfip comment 'Cloudflare IP'; done

  ufw reload > /dev/null

  # OTHER EXAMPLE RULES
  # Retrict to port 80
  #for cfip in `cat /tmp/cf_ips`; do ufw allow proto tcp from $cfip to any port 80 comment 'Cloudflare IP'; done

  # Restrict to port 443
  #for cfip in `cat /tmp/cf_ips`; do ufw allow proto tcp from $cfip to any port 443 comment 'Cloudflare IP'; done

  # Restrict to ports 80 & 443
  # for cfip in `cat /tmp/cf_ips`; do ufw allow proto tcp from $cfip to any port 80,443 comment 'Cloudflare IP'; done
  ```
  Add this to crontab to run daily.
  ```bash
  $ sudo crontab -e
  ```
  add this
  ```
  0 0 * * * /home/pi/.ufw/cloudflare-ufw.sh
  ```
  
  ### Source
  https://github.com/Paul-Reed/cloudflare-ufw
