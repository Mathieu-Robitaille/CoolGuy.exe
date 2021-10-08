# start the camera, note that we need to pass through video devices,
# and we want our user ID and group to have permission to them
# you may need to `sudo groupadd $USER video`

docker run --rm -it --name=tf-test \
  -u $(id -u):$(id -g) \
  --gpus all \
  --device /dev/nvidia0 --device /dev/nvidia-uvm \
  --device /dev/nvidia-uvm-tools --device /dev/nvidiactl \
  -u "$(id -u):$(getent group video | cut -d: -f3)" \
  $(find /dev -name 'video*' -printf "--device %p ") \
  -v "/home/jm/git/CoolGuy.exe/fakecam:/data/" \
  fakecam-python-bodybix:latest

# This is for testing things
docker run --rm -it --name=tf-test \
  -u $(id -u):$(id -g) \
  --gpus all \
  --device /dev/nvidia0 --device /dev/nvidia-uvm \
  --device /dev/nvidia-uvm-tools --device /dev/nvidiactl \
  -u "$(id -u):$(getent group video | cut -d: -f3)" \
  $(find /dev -name 'video*' -printf "--device %p ") \
  -v "/home/jm/git/CoolGuy.exe/fakecam:/data/" \
  tensorflow/tensorflow:latest-gpu
