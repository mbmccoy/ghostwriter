from adafruit_blinka.board.raspberrypi.raspi_40pin import pin
import time
import neopixel

# GPIO.XX =  pin.DXX


def main():
    pixels = neopixel.NeoPixel(pin.D18, 64)
    pixel_value = [0, 0, 0]
    for i in range(1000):
        pixel_value = (pixel_value[0] + i, pixel_value[1] + i % 2, pixel_value[2] + i %3)
        pixels[0] = pixel_value
        time.sleep(0.01)
        time.sleep(0.01)


if __name__ == "__main__":
    main()
