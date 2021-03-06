from adafruit_blinka.board.raspberrypi.raspi_40pin import pin
import time
import neopixel

# GPIO.XX =  pin.DXX


def main():
    pixels = neopixel.NeoPixel(pin.D18, 16 * 16, brightness=0.05)
    try:
        run(pixels)
    finally:
        for i in range(pixels.n):
            pixels[i] = [0, 0, 0]


def run(pixels):
    n = pixels.n
    for i in range(n):
        pixel_value = (100 % 256, (2 * i) % 256, (128 - 2 * i) % 256)
        pixels[i % pixels.n] = pixel_value


if __name__ == "__main__":
    main()
