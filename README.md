# ghostwriter

## Setting up python on a dev machine

We use virtual environments so that we can get as close to a reproducible
image as possible with the RPi. To get set up, simply run 

```bash
make requirements
```

This will take a while since it clones and builds `opencv` from source.

## Setting up python on the RPi

On the Raspberry Pi, we can set up everything using the command

```bash
make pi-setup
```

*Important* This command is very long-running due to the opencv build step. 
If you are using SSH to connect to the pi, consider using `screen` or other 
tool to ensure that the command is not terminated before it completes the 
build.


## Tests

To run the tests in a docker container 

```bash
make test
```

These tests are also run in CI.
