# port-randomizer
a simple proxy that randomize the input or output port

given a input or output port range, the proxy will transfer all traffic from/to a pseudo random port
given a similar seed multiple instance will open the same ports (can be used to add a bit of randomness in your ports :p)

#### Remark:
using both input and output ranges is possible but I am not sure of what it could achieve.


## tldr:
```
port_randomizer.py -i 10000:12000 -o 443 --seed 432135464 --schedule hourly
```

## parameters:
* `-h` `--help` display the help
* `-i` `--input` input port or port range
* `-o` `--output` output port or port range
* `--seed` the seed used for replayability (or synchronicity if a `schedule` is used)
* `--schedule` the schedule for port switching. For synchronicity ensure the machine have a proper clock
* `-d` add debug logs

## Example use case:

you have a service running on port 443 but wish to lower/spread this port usage for whatever reason.  

On the client side set your client instance as proxy with the following parameters:
```
port_randomizer.py -i 443 -o 10000:12000 --seed 1122334455 --schedule hourly
```

then expose your service behind this same proxy using the following configuration:
```
port_randomizer.py -o 443 -i 10000:12000 --seed 1122334455 --schedule hourly
```

both machines will communicate using a random port between 10000 and 12000 changing seamlessly every hour.
