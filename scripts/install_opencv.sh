#!/usr/bin/env bash
# Need  to run with `sudo`
# From: https://pimylifeup.com/raspberry-pi-opencv/
set -e
apt update
apt upgrade
apt install -y \
  cmake \
  build-essential \
  pkg-config git \
  libjpeg-dev \
  libtiff-dev \
  libpng-dev \
  libwebp-dev \
  libopenexr-dev \
  libavcodec-dev \
  libavformat-dev \
  libhdf5-dev \
  libswscale-dev \
  libv4l-dev \
  libxvidcore-dev \
  libx264-dev \
  libdc1394-22-dev \
  libgstreamer-plugins-base1.0-dev \
  libgstreamer1.0-dev \
  libgtk-3-dev \
  libqtgui4 \
  libqtwebkit4 \
  libqt4-test \
  python3-pyqt5 \
  libatlas-base-dev \
  liblapacke-dev \
  gfortran \
  python3-dev \
  python3-pip \
  python3-numpy

apt install -y \
  libjasper-dev \
  libhdf5-103

