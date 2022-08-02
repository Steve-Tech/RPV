# Remote Pi Vehicle
A ‘Remote Pi Vehicle’ (R.P.V.) that could be equipped with a camera and sensors, that can then be controlled from a web server over Wi-Fi.

## Parts I Used:
|Qty|Name|Jaycar Cat. No|
|--|--|--|
||Red Wire|[WH3000](https://www.jaycar.com.au/p/WH3000)|
||Black Wire|[WH3001](https://www.jaycar.com.au/p/WH3001)|
||3.0mm Black Heatshrink|[WH5532](https://www.jaycar.com.au/p/WH5532)|
|2|White 5mm LED|[ZD0196](https://www.jaycar.com.au/p/ZD0196)|
|4|Yellow 5mm LED|[ZD0166](https://www.jaycar.com.au/p/ZD0166)|
|2|White 5mm Cree LED|[ZD0290](https://www.jaycar.com.au/p/ZD0290)|
|2|Red 5mm Cree LED|[ZD0293](https://www.jaycar.com.au/p/ZD0293)|
|1|3.3 Ohm 1/4 Watt Resistors - 8 Pack|[RR1514](https://www.jaycar.com.au/p/RR1514)|
|1|51 Ohm 1/2 Watt Resistors - 8 Pack|[RR0541](https://www.jaycar.com.au/p/RR0541)|
|1|43 Ohm 1/2 Watt Resistors - 8 Pack|[RR0539](https://www.jaycar.com.au/p/RR0539)|
|2|18650 2600mAh Li-ion Protected Battery|[SB2299](https://www.jaycar.com.au/p/SB2299)|
|2|Single 18650 Battery Holder|[PH9205](https://www.jaycar.com.au/p/PH9205)|
|1|DC Voltage Regulator|[XC4514](https://www.jaycar.com.au/p/XC4514)|
|1|L293D Dual Full Bridge Motor Driver IC|[ZK8880](https://www.jaycar.com.au/p/ZK8880)|
|1|5MP Night Vision Camera for Raspberry Pi|[XC9021](https://www.jaycar.com.au/p/XC9021)|
|1|CCS811B Air Quality Sensor|[XC3782](https://www.jaycar.com.au/p/XC3782)|
|1|4 Wheel Drive Motor Chassis Robotics Kit|[KR3162](https://www.jaycar.com.au/p/KR3162)|
|1|Raspberry Pi 3A+|

## Pin Config
#### Raspberry Pi
|Item|BCM GPIO Pin|Physical Board Pin|
|--|--|--|
|L293 Pin 2|5|29|
|L293 Pin 7|6|31|
|L293 Pin 9|12|32|
|L293 Pin 10|23|16|
|L293 Pin 15|24|18|
|L293 Pin 1|13|33|
|L293 Pin 16|3v3|17|
|L293 Pin 4*|GND|20|
|Front Lights|17|11|
|Front Left Indicator|27|13|
|Front Right Indicator|22|15|
|Back Lights|26|37|
|Back Left Indicator|20|38|
|Back Right Indicator|21|40|
|LED Ground|GND|30|
|I²C Power|3v3|1|
|I²C Ground|GND|9|
|I²C Wake/Ground**|GND|14|
|I²C SDA|2|3|
|I²C SCL|3|5|
|Regulator 5V|5v|4|
|Regulator Ground|GND|6|

\* Pin is redundant in theory, since it is grounded through the regulator.

\*\* The CCS811B requires a grounded wake pin to operate.

#### L293
|Item|L293 Pin|
|--|--|
|Battery Positive|8|
|Battery Negative|12|
|Left Motors|3, 6|
|Right Motors|11, 14|

Pins 4, 5, 13, 12 are all ground and therefore interchangeable, but I used the ones mentioned.

#### LED Series Resistor
|LED|Minimum Resistor|Used Resistor|
|--|--|--|
|White 5mm LED|3R3|3R3|
|Yellow 5mm LED|50R|51R|
|White 5mm Cree LED|3R3|3R3|
|Red 5mm Cree LED|40R|43R|

Calculate the minimum required series resistor using (Vs-Vf)/If or using [a calculator](https://www.digikey.com.au/en/resources/conversion-calculators/conversion-calculator-led-series-resistor).

#### Notes
The battery was also hooked up to the input of the 5v regulator, in order to power the Raspberry Pi.

---

This project is licensed under the terms of the MIT license.