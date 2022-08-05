# lifx smart bulb controller

Tested with LIFX Original 1000. May work for other models.
Since we are running in the host network to be able to discover 
the devices set the `PORT` variable if 80 is already used.

## API

Documentation can be found in `/docs`.

Endpoints:
- `[GET] /discover` returns discovered devices
- `[POST] /readings` data={"ip": "ip", "mac": "mac_addr"}, retrieve measurements
- `[POST] /label` data={"ip": "ip",  "mac": "mac_addr", "name": "name"}, set new label for device
- `[POST] /switch` data={"ip": "ip", "mac": "mac_addr"}, on->off OR off->on the given device
- `[POST] /info` data={"ip": "ip", "mac": "mac_addr"}, retrieve device information
- `[GET] /metrics` prometheus metrics

## Prometheus metrics

Provides metrics of discoverable smart devices and
assigns labels according to the label field.
Point the scraper to /metrics.

Discovery of devices runs every 30s. 
For other value set the env variable `DISCOVERY_PERIOD`.
Values are updated every 10s. 
For other value set the env variable `UPDATE_PERIOD`

## To run

with docker
```commandline
docker build -t lifx-controller src/
docker run -d --network host lifx-controller
```

with docker-compose
```commandline
docker-compose build
docker-compose up -d
```

with kubernetes
```commandline
kubectl apply -f https://raw.githubusercontent.com/bmgalhardo/lifx-rest-controller/main/manifest.yml -n <namespace>
```
