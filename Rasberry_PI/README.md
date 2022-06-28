# Rasberry-Pi-can-bus-connection
The method that allow rasberry pi 4B and 3B connect external device via can bus

# notice 
Raspberry Pi is not support can bus in default hardware, u may need to add a CAN- Hat or the MCP2515 can tranceiver for this work. The Pi will be connected to the Tranceiver via CAN Bus 

# Installation (Tested in Oi 4B and 3B only
Install BCM2835
```shell
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
tar zxvf bcm2835-1.60.tar.gz 
cd bcm2835-1.60/
sudo ./configure
sudo make
sudo make check
sudo make install
```
Install Wiring Pi
```shell
sudo apt-get install wiringpi
(optional)wget https://project-downloads.drogon.net/wiringpi-latest.deb
(optional)sudo dpkg -i wiringpi-latest.deb
gpio -v
```
output should be like this 
```shell 
gpio version: 2.50
Copyright (c) 2012-2018 Gordon Henderson
This is free software with ABSOLUTELY NO WARRANTY.
For details type: gpio -warranty

Raspberry Pi Details:
  Type: Unknown17, Revision: 04, Memory: 0MB, Maker: Sony 
  * Device tree is enabled.
  *--> Raspberry Pi 4 Model B Rev 1.4
  * This Raspberry Pi supports user-level GPIO access.
```

python package install
```shell
#python2
sudo apt-get update
sudo apt-get install python-pip
sudo apt-get install python-pil
sudo apt-get install python-numpy
sudo pip install RPi.GPIO
sudo pip install spidev
sudo pip2 install python-can
sudo apt-get install can-utils
#python3
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install spidev 
sudo pip3 install python-can
sudo apt-get install can-utils
```

If you use ubuntu 20.04 or 18.04 the default /boot/config.txt should enable the spi and i2c with a line like 
```shell 
dtparam=spi=on
```
if not add the following line in /boot/config.txt
```shell    
dtparam=spi=on
dtoverlay=mcp2515-can1,oscillator=16000000,interrupt=25
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=23
```
then reboot 
```shell 
sudi reboot
```

Check the interface with 
```shell
dmesg | grep spi
```
![](https://github.com/PolyU-Robocon/Rasberry-Pi-can-bus-connection/blob/main/2-CH-CAN-HAT-SPI-Init.png)

Finally, config the can conection
```shell
sudo ip link set can0 up type can bitrate 1000000
sudo ip link set can1 up type can bitrate 1000000
sudo ifconfig can0 txqueuelen 65536
sudo ifconfig can1 txqueuelen 65536
```

more info at https://www.kernel.org/doc/Documentation/networking/can.txt

Check config 
```shell
ifconfig
```
![](https://github.com/PolyU-Robocon/Rasberry-Pi-can-bus-connection/blob/main/800px-2-CH-CAN-HAT-connect.jpg)

Tryout the connection via: </br>
First terminal 
```shell
candump can0
```
Second Termainal
```shell
cansend can1 000#11.22.33.44
```

Example program for python code </br>
receive.py and send.py (run it in serperate terminal) </br>

## Others
use with c620 driver: </br>
https://blog.csdn.net/weixin_44024557/article/details/117674473

WTF is can bus:</br>
https://www.ni.com/en-us/innovations/white-papers/09/can-physical-layer-and-termination-guide.html

Source: </br>
https://github.com/linux-can/can-utils

Other documentation:</br>
https://www.can-cia.org/fileadmin/resources/documents/proceedings/2012_kleine-budde.pdf

Python socketcan API:</br>
https://python-can.readthedocs.io/en/master/interfaces/socketcan.html

Tutorial:</br>
https://blog.mbedded.ninja/programming/operating-systems/linux/how-to-use-socketcan-with-the-command-line-in-linux/

