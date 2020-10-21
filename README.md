# ghostwriter

## Setting up python on a dev machine

We use virtual environments so that we can get as close to a reproducible
image as possible with the RPi. 

```bash
make venv
```

## Setting up python on the RPi

On the Raspberry Pi, we can set up everything using

```bash
make pi-setup
```

## Tests

To run the tests in a docker container 

```bash
make test
```


