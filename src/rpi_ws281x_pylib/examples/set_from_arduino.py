import serial
from LED_client import LEDClient


def main():
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)

    print('[SCRIPT]> Waiting for device')
    print(f'[SCRIPT]> Connected to {ser.name}\n')

    lc = LEDClient()
    lc.connect()

    while True:
        val = str(ser.readline().decode().strip('\r\n'))  # Capture serial output as a decoded string
        if val:
            print(f"[RECV]> {val}", end="\n", flush=True)

        if val == 'FONA Ready':
            print("[SCRIPT]> Ready to receive commands.\n")
        elif val.startswith("TEXT: "):
            try:
                hue = int(val[6:])
                lc.set_all((int(hue / 360 * 255), 255, 30), color_space='hsv')
            except ValueError:
                print("[SCRIPT]> Wrong command!")


if __name__ == '__main__':
    main()

