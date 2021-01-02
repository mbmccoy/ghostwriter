# ghostwriter

## Installation

We use virtual environments so that we can get as close to a reproducible
image as possible with the RPi. To get set up, simply run 

```bash
make requirements
```

This will take a while since it clones and builds `opencv` from source. 

*Important* On the RPi, this command is very long-running due to the opencv 
build step. If you are using SSH to connect to the pi, consider using 
`screen` or other tool to ensure that the command is not terminated before 
it completes the build.

## Start up
- start the production environment:
```bash
make pi-setup
```
- run "hello world" for LEDs from ghostwriter/pixel with `sudo`:
`sudo $(which python) hello_world.py`


## Tests

To run the tests in a docker container 

```bash
make test
```

These tests are also run in CI.


## Linting

We use `black`. To fix your files locally, just run `make lint`. If you don't
want changes, run `make lint-check` (this is what's run in CI).


# Troubleshooting


## raspberry pi 3b+

- I've verified that LEDs are correctly wired and powered, but my LEDs randomly blink when running 'hello_world.py'. 

Solution 1: Disable the audio drivers.  The audio drivers can interfere with the gpio messages to the LEDs, causing erratic output.  Navigate to `/boot/config.txt` and make the following edits:

```bash
hdmi_force_hotplug=1
dtparam=audio=off
```
Solution 2: if you are using a voltage shifter, verify that all components (pi/3v3,5v,lights) have a common ground.  Messages can be corrupted from "floating ground" issues.

## M1 Mac

See [here](./docs/M1.md) for details.
