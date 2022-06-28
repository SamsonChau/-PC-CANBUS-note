# USB_CAN adaptor for all PC
USB-TTL TO CAN Module from witmotion</br>

SPECIFICATION: SPECIFICATION</br>
Model:USB TO CAN</br>
Description:Serial port to CAN module</br>
Enterprise quality system standard: ISO9001:2016</br>
Sensor production standard：GB/T191SJ 20873-2016</br>
Criterion of detection：GB/T191SJ 20873-2016</br>

This module is convert TTL signals into CAN signals,using the serial port as the interface of
the embedded system,simple date transfer,no need to learn CAN protocol,shorten development
cycles and reduce development costs,module compatible with 3.3V, 5v power supply,small size,
half-hole process, easier to embed in the system


The module is equipped with a 32-bit STM32 processing chip and a CAN level conversion
chip. 14 sets of shielding filters,each with five frame filtering methods.Parameters set to AT
command set mode, instructions simple and refined, only 6 instructions.

## Hardwareconnection
![](https://github.com/PolyU-Robocon/Rasberry-Pi-can-bus-connection/blob/USB_CAN_adaptor/CANbus%20pin.png)

TX-> CANH</br>
RX-> CANL</br>

## Spec
1) Voltage:3.3~5V
2) Consumption current:5.5~6mA
3) Volume:10mm*10mm*5mm
4) Pad pitch:up and down 2mm,left and right 10mm
5) Baud rate: serial port: 4800 - 406800kBps, CAN: 4K - 1MBps
6) Offline self-recovery function
7) 14 sets of shielding filters
8) The parameter can be set by AT command and saved after power down.
9) Hardware, software two restore default parameters

### TTL_Driver
Install the USB-TTL driver ch340.</br>
The drive：</br>
CH340:https://wiki.wit-motion.com/english/doku.php?id=communication_module

## Restore Factory Setting
Operation instructions for restoring default parameters:


Method 1 hardware recovery:First, the CFG pin of the module was lowered(followed by
GND)for 3-5 seconds, then open the parameter set software and select port number, configure
baud rate of the serial port(default 9600), then open the serial port and the PC software
automatically read the module parameters,this method is used without knowing baud rate of serial
port.


Method 2 software recovery:Open the parameter setting software, select port
number,configure baud rate of the serial port(default 9600), click restore default on the PC
software,the module return to OK.

## debug software 
PC software for config: </br>
https://github.com/PolyU-Robocon/Rasberry-Pi-can-bus-connection/blob/USB_CAN_adaptor/PC%20Software/CANToUART/CANToUART.exe


Serial debug tools: </br>
https://github.com/PolyU-Robocon/Rasberry-Pi-can-bus-connection/blob/USB_CAN_adaptor/serial_port_assistantserial_port_debugging_assistant/SerialPortUtility.exe


python program(work in progress):</br>
https://github.com/PolyU-Robocon/Rasberry-Pi-can-bus-connection/blob/USB_CAN_adaptor/ttl2can/src/CAN_Node.py

## other tutorials
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
