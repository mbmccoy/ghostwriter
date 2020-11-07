from adafruit_blinka.board.raspberrypi.raspi_40pin import pin
import time
import neopixel

# GPIO.XX =  pin.DXX


def main():
    pixels = neopixel.NeoPixel(pin.D18, 1)
    for i in range(10):
        pixels[0] = (128, 0, 0)
        time.sleep(0.25)
        pixels[0] = (0, 0, 0)
        time.sleep(0.25)


if __name__ == "__main__":
    main()
