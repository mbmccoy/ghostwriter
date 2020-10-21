# ghostwriter

## Setting up python on a dev machine

We use Docker so that we can get as close to a reproducible
image as possible with the RPi. To build the `ghostwriter` image,
simply run 

```bash
make docker
```

## Setting up python on the RPi

On the Raspberry Pi, we won't use Docker; instead, we'll use
virtual environments. We can get all set up using 

## Tests

To run the tests in a docker container 

```bash
make test
```


