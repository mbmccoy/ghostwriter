#!/usr/bin/env bash
set -ex
# Need  to run with `sudo`
# Cribbed from https://pimylifeup.com/raspberry-pi-opencv/

# check if it is a raspberry pi, because we'll need a special ruby first
R_PI=$(python -c "import platform; print('raspberrypi' in platform.uname())")

set -e

mkdir -p build && pushd build

if [ "$R_PI" = "True" ] ; then
  # Additional RPi packages not available on ubuntu
  sudo apt update && apt upgrade -y && apt install -y \
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
    python3-numpy \
    libjasper-dev \
    libhdf5-103

  # Change swapfile size
  cp /etc/dphys-swapfile ./dphys-swapfile.backup
  sed 's/^CONF_SWAPSIZE=100/CONF_SWAPSIZE=2048/g' /etc/dphys-swapfile > ./dphys-swapfile.new
  sudo cp ./dphys-swapfile.new /etc/dphys-swapfile
  sudo systemctl restart dphys-swapfile
else
  sudo apt install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    gfortran \
    openexr \
    libatlas-base-dev \
    python3-dev \
    python3-numpy \
    libtbb2 \
    libtbb-dev \
    libdc1394-22-dev \
    libopenexr-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev
fi

git clone https://github.com/opencv/opencv.git || echo "OpenCV already cloned..."
git clone https://github.com/opencv/opencv_contrib.git || echo "OpenCV contrib already cloned..."

mkdir -p opencv/build && pushd opencv/build

if [ "$R_PI" = "True" ] ; then
  cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D ENABLE_NEON=ON \
      -D ENABLE_VFPV3=ON \
      -D BUILD_TESTS=OFF \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
      -D BUILD_EXAMPLES=OFF ..
else
  cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D BUILD_TESTS=OFF \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
      -D BUILD_EXAMPLES=OFF ..
fi

make -j$(nproc)

sudo make install
sudo ldconfig

popd
if [ "$R_PI" = "True" ] ; then
  # Clean up swapfile size
  sudo cp ./dphys-swapfile.backup /etc/dphys-swapfile
  sudo systemctl restart dphys-swapfile
fi

popd
cp ./build/opencv/build/python_loader cv2
