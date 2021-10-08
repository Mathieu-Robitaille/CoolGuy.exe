# This seems to create nvidia-uvm?
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
sudo modprobe v4l2loopback devices=1 video_nr=20 card_label="v4l2loopback" exclusive_caps=1

