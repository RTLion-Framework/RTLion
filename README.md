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
pyrlsdr is written in [Python2.7](https://pythonclock.org/) and wraps most of the functions of librtlsdr successfully in order to provide a _more Pythonic API_.

`RTLion` project uses pyrtlsdr to communicate with the RTL-SDR device. (main reason for the need of Python2.7) Also it can be described as a framework due to the implementation of various features other than the frequency scanner. The common structure of the project is appropriate for adding new features too.
`RTLion Framework` has a [Flask](https://flask-socketio.readthedocs.io/en/latest/)-[SocketIO](https://flask-socketio.readthedocs.io/en/latest/) based Web interface which houses it's features there. Web interface preferred to the command line interface for facilitating the usage and supporting remote operations.
[Matplotlib](https://matplotlib.org/) used for creating graphs, more specifically `pylab` [psd](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.psd.html) (Power Spectral Density) method mostly used for converting the complex samples (stored in a `numpy` array) to FFT graphs.

Main purpose of the RTLion Framework is creating a framework for RTL2832 based DVB-T receivers and supporting various features such as spectral density visualizing and frequency scanning remotely. These features are provided on the Web interface and accessible via the RTLion server or the [RTLion Android App](https://github.com/RTLion-Framework/RTLion-app) for RTL-SDR & IoT applications.

## Installation

### Dependencies

* [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)
* [Matplotlib](https://matplotlib.org/)
