CoolGuy.exe
-----------

This is a tool to replace your background with a gif or jpg (realistically it could be another image format but I have not tested it....)

I'm not a python dev (or really even a dev) by trade so there are some crimes commited in here, I dont really know what I'm doing.
If you do spot a crime I'm more than happy to take feedback.

Installation
------------

- You need nvidia's container runtime, [here](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).
  - On archlinux ```yay nvidia-container-runtime``` not the -bin one  
- You need to install v4l2loopback. 
- Run this ```sudo modprobe v4l2loopback devices=1 video_nr=20 card_label="v4l2loopback" exclusive_caps=1```. 
  - This creates a webcam device we send data to.
- Run the docker compose file.
- Use vlc to check your camera is working [Media -> Open Capture Device -> video device /dev/video20]

TODO
----

- Allow use of other image formats.
- Allow use of video formats.
- Make webpage that allows you to upload compatible background formats.
- Finish effects. Maybe even extend them to be able to be generated in the webpage?
- Test the performance of different segments of code, optimise them as much as possible
  - We might not need to get the mask every frame, but only every second frame.
- Change the implementation of image_handler to an abstract class and extend it for video and streams (and other image types if they need that)
- Fix the gross compositing code

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

You'll also need to configure ```/etc/docker/daemon.json``` like so
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