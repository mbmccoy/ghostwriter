sudo apt install v4l-utils v4l2loopback-utils obs-studio v4l2loopback-dkms
sudo modprobe v4l2loopback devices=1 card_label="loopback 1" exclusive_caps=1,1,1,1,1,1,1,1

ffmpeg -re -f live_flv -i udp://localhost:12345 -f v4l2 /dev/video1
