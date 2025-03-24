# plants-grow

## .env file content

| Variable                  | Mandatory |  type  |                      Description                        |
|---------------------------|-----------|--------|---------------------------------------------------------|
| `THERMISTOR`              |   True    | `bool` | Thermistor is present(true) or should be mocked         |
| `PHOTORESISTOR`           |   True    | `bool` | Photoresistor is present(true) or should be mocked      |
| `CAMERA`                  |   True    | `bool` | USB camera is present(true) or should be mocked         |
| `BATTERY_READ_INTERVAL_M` |   False   | `int`  | Interval between reading battery status (in minutes)    |

## How to
1. Create `.env` file with variables mentioned above
1. `make build-base` before building images - needed just once
1. `make build` to build all
1. `make start` to start all
