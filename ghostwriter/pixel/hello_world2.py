"""
A debug script that should make N pixels change from red -> green -> blue over a few seconds.

Note that the color bit depth decreases as brightness decreases and the rate is limited
by the call to `pixels.fill`, even if inc = 0
"""
from adafruit_blinka.board.raspberrypi.raspi_40pin import pin
import time
import neopixel

# number of LEDs; fewer than available is OK
N = 16*16
# brightness parameter: increase to ~1 if you see strange behavior
brightness = 1
# time increment in sec; LEDs response time is not fast and decreases with num LEDs
inc = .0005

def test():
    pixels = neopixel.NeoPixel(pin.D18, N, brightness=brightness)
    # red to green
    for j in range(255):
        pixels.fill((255-j,j, 0))
        time.sleep(inc)
    # green to blue
    for j in range(255):
        pixels.fill((0, 255-j,j))
        time.sleep(inc)


if __name__ == "__main__":
    print("script started")
    test()
    print("script finished")
