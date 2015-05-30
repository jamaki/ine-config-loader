# ine-config-loader
Loads INE CCIE configs onto CSR Routers
Author: Nick Shaw (www.geekynick.co.uk)

This script takes the INE CCIE configs, and applies them to CSR1000v's using telnet.

In my environment I have the CSRs in a VMware environment with network attached serial ports. The configuration for the serial ports is stored in the JSON file included in this repo. Also, there are no usernames and passwords in my environment either.

I have not included the INE configs in this repo for 2 reasons:
  1. They are not mine. I have no affiliation with INE, I am just a user of their materials.
  2. They could change, so it's probably best to get a fresh copy.

Getting them is easy...from the same folder as the script is stored, run these commands:
wget http://labs.ine.com/documents/configs/ine.ccie.rsv5.workbook.initial.configs.zip
unzip ine.ccie.rsv5.workbook.initial.configs.zip

The only other thing you need is a file called "flash:blank-cfg.cfg" to exist on your router. On mine, that has things like "no ip domain lookup" and other useful basics. It is used as a rollback starting point between configuration changes.

Feel free to improve, fork, do whatever. I mostly did this for me - it's probably not very universal, but it's here if it helps!

