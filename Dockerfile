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
    build-base \
    freetype-dev \
    libpng-dev \
    libc-dev \
    libusb-dev \
    make \
    cmake
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
ADD https://api.github.com/repos/radiowitness/librtlsdr/git/refs/heads/master version.json
RUN git clone -b master https://github.com/radiowitness/librtlsdr.git /app/librtlsdr
RUN mkdir /app/librtlsdr/build
RUN cmake /app/librtlsdr/ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON
RUN make
RUN make install
RUN pip install numpy flask-socketio pyrtlsdr matplotlib peakutils
CMD ["python", "RTLion.py"]
