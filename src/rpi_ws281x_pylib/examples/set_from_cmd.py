import time

from rpi_ws281x_pylib import LEDClient


def main():

    leds = LEDClient()
    leds.connect()
    leds.set_all((0, 0, 0))

    while True:
        user_input = input("Enter color in form 'R G B' [0 - 255] > ")
        user_color = [int(x) for x in user_input.split( )]
        leds.set_all(user_color)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("LED Client exited.")
