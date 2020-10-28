#!/usr/bin/env bash
set -ex

FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${FILE_DIR}/.."
VENV_DIR="${BASE_DIR}"/venv

source venv/bin/activate
PYTHON3_EXECUTABLE="$(command -v python3)"
PYTHON_INCLUDE_DIR="${VENV_DIR}"/include
PYTHON_VERSION="$(python ./scripts/python_info.py --version)"
PYTHON_LIBRARY=$(python ./scripts/python_info.py --library)
OPENCV_PYTHON3_INSTALL_PATH="${VENV_DIR}"/lib/python"${PYTHON_VERSION}"/site-packages

R_PI=$(python ./scripts/python_info.py --raspberry-pi)

mkdir -p build && pushd build

if [ "$R_PI" = "True" ] ; then
  # Additional RPi packages not available on ubuntu
  sudo apt update && sudo apt upgrade -y && sudo apt install -y \
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

CMAKE_PYTHON_FLAGS="-D BUILD_opencv_python3=ON \
      -D BUILD_opencv_python2=OFF \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D INSTALL_CREATE_DISTRIB=ON \
      -D PYTHON_DEFAULT_EXECUTABLE=${PYTHON3_EXECUTABLE} \
      -D PYTHON3_EXECUTABLE=${PYTHON3_EXECUTABLE} \
      -D PYTHON_INCLUDE_DIR=${PYTHON_INCLUDE_DIR} \
      -D PYTHON_LIBRARY=${PYTHON_LIBRARY} \
      -D PYTHON3_NUMPY_INCLUDE_DIRS=${OPENCV_PYTHON3_INSTALL_PATH}/numpy/core/include \
      -D OPENCV_PYTHON3_INSTALL_PATH=${OPENCV_PYTHON3_INSTALL_PATH}"

echo "CMAKE_PYTHON_FLAGS" "${CMAKE_PYTHON_FLAGS}"

if [ "$R_PI" = "True" ] ; then
  cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D ENABLE_NEON=ON \
      -D ENABLE_VFPV3=ON \
      -D BUILD_TESTS=OFF \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
      -D BUILD_EXAMPLES=OFF \
      "${CMAKE_PYTHON_FLAGS}" \
       ..
else
  cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D BUILD_TESTS=OFF \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
      "${CMAKE_PYTHON_FLAGS}" \
      -D BUILD_EXAMPLES=OFF ..
fi

make -j"$(nproc)"

sudo make install
sudo ldconfig

popd
if [ "$R_PI" = "True" ] ; then
  # Clean up swapfile size
  sudo cp ./dphys-swapfile.backup /etc/dphys-swapfile
  sudo systemctl restart dphys-swapfile
fi
