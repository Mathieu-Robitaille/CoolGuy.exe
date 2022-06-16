CoolGuy.exe
-----------

This is a tool to replace your background with a gif, image, or mp4.

I'm not a python dev (or really even a dev) by trade so there are some crimes commited in here, I dont really know what I'm doing.
If you do spot a crime I'm more than happy to take feedback.

As a note, my computer has the following specs.
 - AMD Ryzen 7 3800X
 - Nvidia RTX 2080ti

I'm mentionning this due to these being pretty powerful. While this might be "lightweight" on my computer, this will trash some other computers. 
My desktop can crank out 30 fps easily, while my laptop can run about 15 at 50% cpu load.

Installation
------------

- You need nvidia's container runtime, [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).
  - On archlinux ```yay nvidia-container-runtime``` not the -bin one.
  - On ubuntu its super straight forward.  
- You need to install v4l2loopback. 
- Run this ```sudo modprobe v4l2loopback devices=1 video_nr=20 card_label="v4l2loopback" exclusive_caps=1```. 
  - This creates a webcam device we send data to.
- Run the docker compose file.
- Use vlc to check your camera is working [Media -> Open Capture Device -> video device /dev/video20]

USE
------
To change to an existing image (or just use change-background.sh)

```
curl -H "Content-Type: application/json" \
    -X POST \
    --data '{"filename":"$EXISTING-FILENAME"}' \
    http://127.0.0.1:5000/
```

To upload and use a new photo use this

```
curl -H "Content-Type: application/json" \
    -X POST \
    --data '{"url":"https://i.imgur.com/x0RLIVW.gif", "filename":"$NEW-FILENAME"}' \
    http://127.0.0.1:5000/
```

You'll also need to configure ```/etc/docker/daemon.json``` like so (If not on ubuntu)
```
{
    "runtimes": {
        "nvidia": {
            "path": "/usr/bin/nvidia-container-runtime",  "runtimeArgs": []
        }
    }
}
```


Below are some good memes, share them wisely
- https://c.tenor.com/hjhD5wq1jY8AAAAd/no-money-money.gif
- https://c.tenor.com/7QhoA9wcstgAAAAC/confused-no.gif
- https://c.tenor.com/e5SXFKkK43sAAAAC/nick-young-question-marks.gif




curl -H "Content-Type: application/json" -X POST --data '{"lip_color":"blue"}' http://127.0.0.1:9987/

