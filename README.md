HELLO!

Zero effort has been put into this to make it easy to maintain nor read. This is for me to use and you to laugh at.

Installation
------------

- You need nvidia's container runtime, GOOD LUCK!
- You need to edit some of these files. (dirpath in change-background.sh, and path in docker-run)
- You need to install v4l2loopback, and I think thats it?
- run this ```sudo modprobe v4l2loopback devices=1 video_nr=20 card_label="v4l2loopback" exclusive_caps=1```
- Build both containers (check build.sh)
- Start bodypix (check docker-run.sh)
- Start fakecam (check docker-run.sh) This might take ~20 min due to opencv
- use vlc to check your camera is working [Media -> Open Capture Device -> video device /dev/video20]


Ideas:

make webpage that allows you to upload images or gifs and allows you to switch between them instead of the hot bodge

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


You run the container like this

IMAGEDIR = the location you have images and or memes
```
docker run -d \
  --name=fakecam \
  --network=fakecam \
  -u "$(id -u):$(getent group video | cut -d: -f3)" \
  $(find /dev -name 'video*' -printf "--device %p ") \
  -v "$IMAGEDIR:/data/"
  fakecam:latest
```

Below are some good memes, share them wisely
- https://c.tenor.com/hjhD5wq1jY8AAAAd/no-money-money.gif
- https://c.tenor.com/7QhoA9wcstgAAAAC/confused-no.gif
- https://c.tenor.com/e5SXFKkK43sAAAAC/nick-young-question-marks.gif