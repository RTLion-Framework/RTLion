![RTLion](https://user-images.githubusercontent.com/24392180/57021451-ed7cf780-6c34-11e9-8522-84bcd39728d4.png)

# RTLion Framework <a href="https://github.com/RTLion-Framework/RTLion/releases"><img src="https://img.shields.io/github/release/RTLion-Framework/RTLion.svg"/></a>

### Multipurpose RTL-SDR Framework for RTL2832 based DVB-T receivers.

<a href="https://github.com/RTLion-Framework/RTLion/issues"><img src="https://img.shields.io/github/issues/RTLion-Framework/RTLion.svg"/></a>
<a href="https://github.com/RTLion-Framework/RTLion/pulls"><img src="https://img.shields.io/github/issues-pr/RTLion-Framework/RTLion.svg"/></a>
<a href="https://github.com/RTLion-Framework/RTLion/stargazers"><img src="https://img.shields.io/github/stars/RTLion-Framework/RTLion.svg"/></a>
<a href="https://github.com/RTLion-Framework/RTLion/network"><img src="https://img.shields.io/github/forks/RTLion-Framework/RTLion.svg"/></a>
<a href="https://github.com/RTLion-Framework/RTLion/blob/master/LICENSE"><img src="https://img.shields.io/github/license/RTLion-Framework/RTLion.svg"/></a>

Lack of a simple FFT visualizer tool for RTL-SDR was the main reason behind the [rtl_map](https://github.com/KeyLo99/rtl_map) project which was released at [January 30](https://www.rtl-sdr.com/rtl_map-a-simple-fft-visualizer-for-rtl-sdr/) and caught attention of RTL-SDR enthusiasts. Another purpose of that project was creating a `Frequency Scanner` tool that will provide FFT-based power (dB) scanning. So I decided to postpone that feature with a [todo](https://github.com/KeyLo99/rtl_map#todos) and dive into the other RTL-SDR related libraries such as [pyrtlsdr](https://github.com/roger-/pyrtlsdr) for learning new stuff and also for creating that scanning tool.

[pyrtlsdr](https://github.com/roger-/pyrtlsdr) is a wrapper library for [librtlsdr](https://github.com/librtlsdr) that aims turning RTL2832U devices into an `Software Defined Radio`. librtlsdr itself contains main functions for RTL-SDR and have derived tools as `rtl_sdr`, `rtl_fm` etc. (More info can be found at [wiki](https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr))
pyrlsdr is written in Python and wraps most of the functions of librtlsdr successfully in order to provide a _more Pythonic API_. `RTLion` project uses pyrtlsdr to communicate with the RTL-SDR device. 

`RTLion` project can be described as a framework due to the implementation of various features other than the frequency scanner. The common structure of the project is appropriate for adding new features too.
`RTLion Framework` has a [Flask](https://flask-socketio.readthedocs.io/en/latest/)-[SocketIO](https://flask-socketio.readthedocs.io/en/latest/) based Web interface which houses it's features there. Web interface preferred to the command line interface for facilitating the usage and supporting remote operations.
[Matplotlib](https://matplotlib.org/) used for creating graphs, more specifically `pylab` [psd](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.psd.html) (Power Spectral Density) method mostly used for converting the complex samples (stored in a `numpy` array) to FFT graphs.

Main purpose of the RTLion Framework is creating a framework for RTL2832 based DVB-T receivers and supporting various features such as spectral density visualizing and frequency scanning remotely. These features are provided on the Web interface and accessible via the RTLion server or the [RTLion Android App](https://github.com/RTLion-Framework/RTLion-app) for RTL-SDR & IoT applications.

## Installation

### Dependencies

* [pyrtlsdr](https://pypi.org/project/pyrtlsdr/)
  * _[librtlsdr](https://github.com/librtlsdr/librtlsdr)*_
* [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)
* [Matplotlib](https://matplotlib.org/)

[*] _librtlsdr must be installed for pyrtlsdr to access RTL-SDR device._

### Clone the Repository

```
git clone https://github.com/RTLion-Framework/RTLion
```

### Package Installation
Recommended installation:
```
pip3.7 install -r requirements.txt
```
Manual installation:
```
# [Install flask-socketio with pip]
pip3.7 install flask-socketio
# [Install matplotlib with your package manager]
# [Ubuntu]
sudo apt-get install python-matplotlib
# [Arch]
trizen python-matplotlib
```
## Usage
### Command Line Arguments

Command line arguments are not mandatory because it's possible to update settings at the Web interface. But still, RTLion server can be started with the command line arguments.

```
usage: RTLion.py [-h] [-d DEV] [-s SAMPRATE] [-f FREQ] [-g GAIN] [-n N] [-i I] [host:port]
```
Positional Arguments
```
[host:port] -> IP address/hostname and port number for server to listen on (default: 0.0.0.0:8081)
```
Optional Arguments
```
[-h, --help]                        -> show help message and exit
[-d DEV, --dev DEV]                 -> device index (default: 0)
[-s SAMPRATE, --samprate SAMPRATE]  -> sample rate (default: 2048000 Hz)
[-f FREQ, --freq FREQ]              -> center frequency (Hz)
[-g GAIN, --gain GAIN]              -> gain (0 for auto) (default: auto)
[-n N, -num N]                      -> number of the reads (default: -1, inf.)
[-i I, -interval I]                 -> interval between reads (default: 500ms)
```
### Starting RTLion Server

Basically, execute the main file `RTLion.py` using `Python3.7`. (_Command line arguments are optional._)

![Starting RTLion Server](https://user-images.githubusercontent.com/24392180/57334572-cd63a180-7128-11e9-8a9b-291b065d5f25.gif)

### Power Spectrum 

Web interface is accessible with using the RTLion server's host and port information.

![RTLion Main Page](https://user-images.githubusercontent.com/24392180/57165876-05a17200-6e01-11e9-8a87-9be895356617.gif)

After selecting the `Power Spectrum (FFT Graph)` option, it's possible to update settings and create graph. 

![RTLion Graph Page](https://user-images.githubusercontent.com/24392180/57165174-05a07280-6dff-11e9-8fe8-4ff844cc03ee.gif)

Also center frequency can be changed real time via the `range input` element below the graph. 

![RTLion Power Spectrum](https://user-images.githubusercontent.com/24392180/57165414-b4dd4980-6dff-11e9-99ea-8664f0423e5e.gif)


### Frequency Scanner

Frequency scanner aims to find the peaks on a power spectrum for miscellaneous applications with using a sorting method. For doing that it takes 2 important arguments which can be listed as `frequency range` (min. - max.) and `sensitivity`.

RTLion computes frequency range and step size values automatically if `center frequency` parameter is given within the command line. Otherwise, the user should enter the frequency range manually.

![RTLion Frequency Scanner](https://user-images.githubusercontent.com/24392180/57167958-608a9780-6e08-11e9-9403-684a7d09ff61.gif)

`Sensitivity` value determines the count of the frequencies that will selected from the sorted list and can be changed with the range input element. Increasing the sensitivity causes scanned values to increase so it's important to use this parameter correctly depending on what the main goal is. Also it's easy to sight scanned values since RTLion marks them with a `"x"` on the graph.

![Scanning 80 MHz - 102 MHz](https://user-images.githubusercontent.com/24392180/57168107-06d69d00-6e09-11e9-8db0-3cbabdf43096.gif)

![Scan Results of 80 MHz - 102 MHz](https://user-images.githubusercontent.com/24392180/57168165-561ccd80-6e09-11e9-8f8e-b7a3d8222d8b.gif)

### Logs

RTLion Framework provides logging with command line and Web interface.

![Command Line Logging](https://user-images.githubusercontent.com/24392180/57168771-f96ee200-6e0b-11e9-8c72-9ea0840d55f7.gif)


![Web Interface Logging](https://user-images.githubusercontent.com/24392180/57168608-1fe04d80-6e0b-11e9-8e19-6148a10f623d.gif)


## Android Application

It's possible to use RTLion Framework's features on a Android device via the mobile application.
For more info, visit the [RTLion-app](https://github.com/RTLion-Framework/RTLion-app/) repository.

![RTLion App Page](https://user-images.githubusercontent.com/24392180/57368986-28cb7900-7195-11e9-870e-658581bc09f9.png)


## RTLion with Docker

[Dockerfile](https://github.com/KeyLo99/RTLion/blob/master/Dockerfile) provided in the repository for using the RTLion Framework with Docker. Usable with the IoT applications.

### Building the Image

Image can be built on the directory after cloning the repository.

```
docker build -t rtlion .
```

### Running the Container

```
docker run -d --name rtlionfw -p 8081:8081 --privileged -v /dev/bus/usb:/dev/bus/usb rtlion
```

`docker ps` output:

![Docker ps](https://user-images.githubusercontent.com/24392180/57368369-abebcf80-7193-11e9-8581-0806c5a91f5d.jpg)

### Stopping & Removing the Container

```
docker stop rtlionfw
docker rm rtlionfw
```

## IoT

At the IoT side of the project, it's possible to run RTLion server (with or without [Docker](https://github.com/RTLion-Framework/RTLion#rtlion-with-docker)) on a device like Raspberry Pi with the RTL-SDR plugged in and access the RTLion Framework remotely. (This concept can be diversified.)

![IoT Diagram](https://user-images.githubusercontent.com/24392180/57574360-04db9200-7438-11e9-9719-0e8ae576e79b.png)

### Version 1.0

Prototype v1 is designed to be portable with Raspberry Pi 3 model B, RTL-SDR (RTL2832U / 820T2) and external power supply. RTL-SDR is half embedded inside the case and other half is outside for the antenna connection.

![RTLion - IoT Prototype](https://user-images.githubusercontent.com/24392180/57582137-4c5a3080-74c1-11e9-92d8-b4746f9a5efd.png)

It's possible to disconnect RTL-SDR with unplugging the USB from Raspberry Pi.

![RTLion - IoT USB Bus](https://user-images.githubusercontent.com/24392180/57582148-81668300-74c1-11e9-9c32-df8ffb3efd5f.png)

![RTLion - IoT RTL-SDR](https://user-images.githubusercontent.com/24392180/57582244-a4456700-74c2-11e9-8735-7a97b8f89629.png)

RTL-SDR antenna connection is shown below.

![RTLion - IoT Antenna](https://user-images.githubusercontent.com/24392180/57582307-3f3e4100-74c3-11e9-8ed4-5c87c740f480.png)

Device can be powered by the power bank below the case. It shows the battery status with the LED indicator.

![RTLion - IoT Power](https://user-images.githubusercontent.com/24392180/57582280-fb4b3c00-74c2-11e9-9448-6b611b1dfdd5.png)

### Inner Design of Version 1.0

The case contains a fan for cooling the Raspberry Pi and a female USB port for outer devices which leads to a USB connector. This USB adapter connection is required for embedding the RTL-SDR circuit inside the case and getting rid of redundant design of connecting RTL-SDR to the Raspberry Pi's USB port.

![RTLion - IoT Design I](https://user-images.githubusercontent.com/24392180/57582327-a52ac880-74c3-11e9-97a3-dae6cf27ce28.jpg)

![RTLion - IoT Design II](https://user-images.githubusercontent.com/24392180/57582360-17031200-74c4-11e9-983e-dcedaa370456.png)

Of course this prototype design can be improved due to the existence of other Raspberry Pi versions such as Zero.

### Accessing the Server

After [starting the RTLion server](https://github.com/RTLion-Framework/RTLion#starting-rtlion-server) on Raspberry Pi, connection can be made from the Web interface or the [mobile application](https://github.com/RTLion-Framework/RTLion-app#iot) and the RTL-SDR functions can be accessed.

![Starting RTLion Server on RPI](https://user-images.githubusercontent.com/24392180/57583800-e7143880-74dc-11e9-9a12-0479344b0514.png)

#### DVB Driver Issue

librtlsdr can't access the RTL-SDR device when the Linux kernel DVB driver is loaded and shows the warning message below.

```
Kernel driver is active, or device is claimed by second instance of librtlsdr. In the first case, please either detach or blacklist the kernel module (dvb_usb_rtl28xxu), or enable automatic detaching at compile time.
```

Unloading driver solves the issue temporarily.

```
sudo rmmod dvb_usb_rtl28xxu rtl2832
```

Visit [blacklist_dvb_usb_rtl28xxu](https://www.reddit.com/r/RTLSDR/wiki/blacklist_dvb_usb_rtl28xxu) for more info and permanent solution.

## TODO(s)

_Considerable for future versions._
* Implement modulation and audio support (AM/FM)
* Fix step size calculation for not wide frequency ranges
* Make more responsive web interface
* Minimalize the Dockerfile for a lighter build
* Add new features to graphs (saving as png, txt)

## Contribution

RTLion Project is open to contributions.[*](https://github.com/RTLion-Framework/RTLion/CONTRIBUTING.md)

## License

GNU General Public License v3. (see [gpl](https://www.gnu.org/licenses/gpl.txt))

## Credit

Copyright (C) 2019 by KeyLo99 
https://www.github.com/KeyLo99

