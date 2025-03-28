# plants-grow

## .env file content

| Variable                  | Mandatory |  type  |                            Description                                |
|---------------------------|-----------|--------|-----------------------------------------------------------------------|
| `THERMISTOR`              |   True    | `bool` | Thermistor is present(true) or should be mocked                       |
| `PHOTORESISTOR`           |   True    | `bool` | Photoresistor is present(true) or should be mocked                    |
| `CAMERA`                  |   True    | `bool` | USB camera is present(true) or should be mocked                       |
| `BATTERY_READ_INTERVAL_M` |   False   | `int`  | default `30`, Interval between reading battery status (in minutes)    |
| `FONT_SIZE_RATIO`         |   False   | `int`  | default `5`, timestamp font size, relative to picture height          |
| `SENDER`                  |   True    | `str`  | Sender's e-mail address                                               |
| `MAILBOX`                 |   True    | `str`  | mailbox name to use - supported: `GMAIL`                              |

## Prerequisites

### Docker
https://docs.docker.com/engine/install/debian/
https://docs.docker.com/engine/install/linux-postinstall/

### Memory limit
Memory limit support on RPI is disabled by default. In order to enable it edit `/boot/firmware/cmdline.txt`
adding the following to the end of the file: `cgroup_enable=memory swapaccount=1 cgroup_memory=1 cgroup_enable=cpuset`
and reboot

### gvfs-gphoto2-volume-monitor
Even the [author doesn't seem to know why this is started](https://github.com/gphoto/gphoto2/issues/181). It could probably be disabled in some event-driven way,
but this way takes much less dev time and is robust enough

1. Move `./host_files/gphoto2-volume-monitor-killer.sh` to intended location or use it directly:
1. run `chmod +x /path/to/bash_script.sh`
1. run `crontab -e`
1. Add the following to crontab: `@reboot sleep 20 && /path/to/bash_script.sh`
1. `sudo reboot now`

## How to
1. Create `.env` file with variables mentioned above
1. `make build-base` before building images - needed just once
1. `make build` to build all
1. `make start` to start all
