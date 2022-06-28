# Connect ROS to CAN-BUS port with Jetson NX/ TX2 on board computer 
Connect the ros system to CAN-BUS with the socket can and canopen </br>

Can be used on:</be>
* rasberrry pi with MCP2551 can shield
* Jetson Xaiver NX (waiting for testing) with can tranceiver
* Jetson TX2 (waiting for testing)

## Hardware Config 
1. Rasberry PI https://github.com/PolyU-Robocon/PC-CAN-BUS-connection/tree/rasberry_pi_canbus
2. Jetson Jetson Xaiver NX (IGGG-cAN-NX-J17) https://github.com/PolyU-Robocon/IGGG-Connector-Standard/tree/main/CAN%20Bus
3. Jetson TX2 https://forums.developer.nvidia.com/t/how-can-i-use-can-bus-in-tx2/49652/28

## Config the can bus port 
1. Jetsons

Enable kernel support for mttcan(Other required modules are already supported)
```shell
CONFIG_MTTCAN = m (Here mttcan is compiled as a module)
```
Insert CAN BUS subsystem support module.
```shell 
modprobe can
```
Insert Raw CAN protocol module (CAN-ID filtering)
```shell
modprobe can_raw
```
Real CAN interface support (for our case, it is: mttcan)
```shell
modprobe mttcan #dependent module is can_dev: can driver with netlink support
```
CAN interface settings for both the controllers
```shell
ip link set can0 type can bitrate 500000 dbitrate 2000000 berr-reporting on fd on
ip link set up can0
ip link set can1 type can bitrate 500000 dbitrate 2000000 berr-reporting on fd on
ip link set up can1
```
CAN interfaces are up now. Use ifconfig to list all the interfaces which are up.

Installation of user app to check CAN communication
```shell
sudo apt-get install can-utils
```
Commands to run to check CAN packet send/receive
broadcasting a can data packet:
```shell
cansend <can_interface> <can_frame>
```
e.g. cansend can0 123#abcdabcd

Receiving a can data packet:
```shell
candump can_interface
```
e.g. ```candump can1```

Different tools (i.e. cangen, cangw etc) can be used for various filtering options.

To check the interface statistics
```shell
ip -details -statistics link show can0
ip -details -statistics link show can1
```

2. Rasberry PI
tutorial https://github.com/PolyU-Robocon/PC-CAN-BUS-connection/tree/rasberry_pi_canbus

## ROS socketcan config and test
official ROScanopen repo: https://github.com/ros-industrial/ros_canopen/tree/melodic-devel

### ROS package Installation (same for the pi and jetson)
insatll roscanopen
 ```shell 
 sudo apt-get install ros-melodic-ros-canopen
 ```
 ### Test the node
 1. Receive CANBUS data from can0
 run the node (can0)</br>
 on Terminal 1
 ```shell
 roscore
 ```
 on Terminal 2 
 ```shell
 rosrun socketcan_bridge socketcan_to_topic_node
 ```
 on Terminal 3 
 ```shell
 rostopic eho received_messages
 ```
 You should see some thing like this data in integer
 ![](https://github.com/PolyU-Robocon/PC-CAN-BUS-connection/blob/jetson-NX/tx2-ros-can/can_message.png)
 
 if your device have 2 can terminal u can test it by send one message from the other port
 1. open another terminal 
 2. publish a can frame(data & ID in HEX)``` cansend can1 080#11.22.33.44``` 
 you should see a topic will publish in the terminal (data in OCT) 
 
 2. Send data from can0 
 run the node on terminal 1 (run the core first if you are the noob)
 ``` shell
 rosrun socketcan_bridge topic_to_socketcan_node 
 ```
 if u have second interface on your device use can1 to receive the signal </br>
 on other terminal 2 
 ```shell
 candump can1
 ```
 Publish a topic using terminal 3
 ```shell
 rostopic pub /sent_messages can_msgs/Frame '{header:{seq: 0, stamp:{secs: 1000,nsecs: 12200}, frame_id: ''}, id: 34,is_rtr: False, is_extended: False, is_error: False, dlc: 8, data:[00,00,00,00,00,00,00,00]}'
```
You should see a can signal in terminal 2 recieved in can1
``` shell 
   can1  022   [8]  00 00 00 00 00 00 00 00
```

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

