from adafruit_blinka.board.raspberrypi.raspi_40pin import pin
import time
import neopixel

# GPIO.XX =  pin.DXX


def main():
    pixels = neopixel.NeoPixel(pin.D18, 64)
    try:
        run(pixels)
    finally:
        for i in range(pixels.n):
            pixels[i] = [0, 0, 0]


def run(pixels):
    pixel_value = [0, 0, 0]
    for i in range(1000):
        pixel_value = ((pixel_value[0] + i) % 64, (pixel_value[1] + i % 2)%64, (pixel_value[2] + i %3) % 64)
        pixels[i % pixels.n] = pixel_value
        time.sleep(0.01)



if __name__ == "__main__":
    main()
