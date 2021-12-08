#  rpi_ws281x_pylib
Simple client-server python library for rpi_ws281x.

PWM GPIO pins on Raspberry Pi that are used for driving the LEDs require root access. To avoid running everything with sudo, only the server runs priviliged and writes color data to LEDs, while client provides user-friendly functions for drawing on the LED matrix and can be imported elsewhere.

## Installation
1. Clone the base repository: https://github.com/jgarff/rpi_ws281x (This doesn't have to be catkin workspace. It is recommended to make a new directory in /home/user for such packages, e.g. /home/user/CustomPackages)
1. Follow the Build instructions (using Scons) of the base repository
1. Check their Running section to test out the build.
1. Install necessary python packages: `sudo pip3 install rpi_ws281x pyzmq numpy` (Using sudo is important!)
1. Clone this repository (wherever).

## Usage
To test the installation, run `sudo python3 example.py`.

To control the LEDs, first run `sudo python3 LED_server.py`. Then, in a separate process, run `python3 LED_client.py`. Client currently cycles through 32 colors for a few seconds and then exits. In general, you want to import the client to your application, create an instance and then use the API functions to get the desired effects.
