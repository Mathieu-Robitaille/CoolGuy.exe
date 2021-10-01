sudo nvidia-modprobe
sudo modprobe v4l2loopback devices=1 video_nr=20 card_label="v4l2loopback" exclusive_caps=1
docker start bodypix
docker start fakecam
