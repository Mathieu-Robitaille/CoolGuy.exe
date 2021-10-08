HELLO!

Zero effort has been put into this to make it easy to maintain nor read. This is for me to use and you to laugh at.


This replaces your background with your pick of jpg or gif!

Installation
------------

- You need nvidia's container runtime, GOOD LUCK!
- You need to edit some of these files. (dirpath in change-background.sh)
- You need to install v4l2loopback, and I think thats it?
- run this ```sudo modprobe v4l2loopback devices=1 video_nr=20 card_label="v4l2loopback" exclusive_caps=1```
- use vlc to check your camera is working [Media -> Open Capture Device -> video device /dev/video20]

It seems like running this ``` docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi ``` Might fix some devices missing for /dev/nvidia-*?????


Ideas:
----

- Make webpage that allows you to upload images or gifs and allows you to switch between them instead of the hot bodge

To change to an existing image (or just use change-background.sh)

```
curl -H "Content-Type: application/json" \
    -X POST \
    --data '{"filename":"rat.gif"}' \
    http://127.0.0.1:5000/
```

To upload and use a new photo use this

```
curl -H "Content-Type: application/json" \
    -X POST \
    --data '{"url":"https://i.imgur.com/x0RLIVW.gif", "filename":"rat.gif"}' \
    http://127.0.0.1:5000/
```

Below are some good memes, share them wisely
- https://c.tenor.com/hjhD5wq1jY8AAAAd/no-money-money.gif
- https://c.tenor.com/7QhoA9wcstgAAAAC/confused-no.gif
- https://c.tenor.com/e5SXFKkK43sAAAAC/nick-young-question-marks.gif