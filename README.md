# plants-grow

## .env file content

| Variable                  | Mandatory |  type  |                            Description                                |
|---------------------------|-----------|--------|-----------------------------------------------------------------------|
| `THERMISTOR`              |   True    | `bool` | Thermistor is present(true) or should be mocked                       |
| `PHOTORESISTOR`           |   True    | `bool` | Photoresistor is present(true) or should be mocked                    |
| `CAMERA`                  |   True    | `bool` | USB camera is present(true) or should be mocked                       |
| `BATTERY_READ_INTERVAL_M` |   False   | `int`  | default `30`, Interval between reading battery status (in minutes)    |
| `FONT_SIZE_RATIO`         |   False   | `int`  | default `5`, timestamp font size, relative to picture height          |

## Prerequisites

### Memory limit
Memory limit support on RPI is disabled by default. In order to enable it edit `/boot/firmware/cmdline.txt`
adding the following to the end of the file: `cgroup_enable=memory swapaccount=1 cgroup_memory=1 cgroup_enable=cpuset`
and reboot

### gphoto2 on host
Presence of gphoto2 package on host is not required, although it's useful while debugging. If gphoto2 is installed it can
silently claim the camera in the background making the camera unusable the others. To prevent that the following can be done:
1. Create a bash script with content:
```
#!/bin/bash

pkill -f "/usr/libexec/gvfs-gphoto2-volume-monitor"
pkill -f "/usr/libexec/gvfsd-gphoto2"
```
1. run `chmod +x /path/to/bash_script.sh`
1. run `crontab -e`
1. Add the following to crontab: `@reboot /path/to/bash_script.sh`
1. `sudo reboot now`

## How to
1. Create `.env` file with variables mentioned above
1. `make build-base` before building images - needed just once
1. `make build` to build all
1. `make start` to start all


## Memory limit
Memory limit support on RPI is disabled by default. In order to enable it edit `/boot/firmware/cmdline.txt`
adding the following to the end of the file: `cgroup_enable=memory swapaccount=1 cgroup_memory=1 cgroup_enable=cpuset`
and reboot
