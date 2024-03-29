# README for ESP8266 WiFi Module
### Based on knowledge gained from the internet and prototyping
### Note: this is a work in progress

## Basic info
The ESP8266 module we prototyped with is the ESP8266 ESP-01S. Most of the work I've done is based off of [this guide](https://www.instructables.com/ESP8266-WiFi-Module-for-Dummies/). Follow it until step 6 where they have the schematic, following the steps for interfacing with the WiFi module using the USB to Serial programmer (from 362). The schematic is decent, but it is confusing. The pin connections I found that work for interfacing with the default firmware (no flashing yet) are as follows:

### ESP8266 ESP-01S
- VCC: +3.3V
- REST: active low reset button with 10k pull down resistor
- CH\_PD: connected to +3.3V through a 10k pull down resistor
- TX (called UTXD or similar): RX port of USB to Serial programmer
- RX (called URXD or similar): TX port of USB to Serial programmer
- GPIO0: DO NOT CONNECT TO ANYTHING (I have no idea why but it doesn't work when you connect this to power or ground. When flashing the chip this must be connected to ground)
- GPIO2: LED through 150 Ω resistor
- GND: ground rail

Once the circuit is built, open the Arduino IDE. Follow the steps in the tutorial to download the ESP8266 library and connect the serial programmer through a COM port. Then open the serial monitor in the Arduino IDE and make sure the prompt comes up. Set the baud rate to 115200, as this is the default. Now, should have access to the AT instruction set if the default firmware is still installed. Enter the command "AT" into the serial monitor port. If it returns "OK" then you're good. If it doesn't good luck, there isn't a lot of useful information on the internet. 

## AT Commands
A list of all available AT commands is available [here](https://www.espressif.com/sites/default/files/documentation/4a-esp8266_at_instruction_set_en.pdf). Here are some that I used as a proof of concept to make sure that our WiFi module worked.

- AT: status check to see if module is running and can transmit and recieve information
- AT+GMR: returns info about the module
- AT+CWMODE\_DEF=1: configures module to be a station so it can connect to a network (must be done before any connecting)
- AT+CWJAP\_DEF="ssid","password": connects module to a WiFi network with name ssid and given password (saved in flash)
- AT+CWAUTOCONN=1: automatically connects to saved network on startup
- AT+CWQAP: disconnects from the network

Use these to do stuff with WiFi. There are also 3 GPIO ports on here that have their own commands, I haven't messed around with those though. 

The range seems to be really good. I connected the module to my phone's hotspot and walked to the farthest corner of lab, probably 50 feet away, and it was still connected. It should be more than enough for our project. 

## Flashing new firmware
You can also flash new firmware by flashing an Arduino sketch onto the ESP8266 board in the Arduino IDE. As of Wednesday, February 21st, I haven't because I don't want to mess up the default firmware since flashing the chip will erase that. We will have to do it eventaully but I want to prepare more before I do it. It's also posible to get the default firmware back but it is a long and annoying procedure. This is a work in progress. 

## ESP8266 SMT Module - ESP-12F
### Work in progress
This is the actual module we bought. The Digikey page is [here](https://www.digikey.com/en/products/detail/adafruit-industries-llc/2491/5761206) and the datasheet is [here](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/308/2491_Web.pdf). I'll look into it next, but we have a good proof of concept here. 

We will probably need some special circuitry in the beacon's PCB for this module. 
