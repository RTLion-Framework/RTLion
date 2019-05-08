
FROM python:3.7-alpine

MAINTAINER [.k3]

COPY . /app
WORKDIR /app
RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/latest-stable/main" > /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/latest-stable/community" >> /etc/apk/repositories
RUN apk --no-cache --update-cache add \
    gcc \
    git \
    gfortran \
    python \
    python-dev \
    py-pip \
    build-base \
    wget \
    freetype-dev \
    libpng-dev \
    openblas-dev \
    libc-dev \
    libusb-dev \
    make \
    cmake \
    bash
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

ADD https://api.github.com/repos/radiowitness/librtlsdr/git/refs/heads/master version.json
RUN git clone -b master https://github.com/radiowitness/librtlsdr.git /usr/local/share/librtlsdr
RUN mkdir /usr/local/share/librtlsdr/build

RUN cmake /usr/local/share/librtlsdr/ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON
RUN make
RUN make install

RUN pip install numpy flask-socketio pyrtlsdr matplotlib
CMD [ "python", "RTLion.py"]
