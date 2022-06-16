ToDo
=====

Until I find a standard format for this I will make my own similar to the change log.

## [ Work In Progress ]

### Adding

 - Facial recognition: 
   - The face_recognition lib in python exposes some dlib stuff so we can track faces and get facial landmarks.
   - Right now this is really expencive to run... (The whole thing is, but this is especially expencive)

- Auto profiler:
   - Test the performance of different segments of code, optimise them as much as possible
   - We might not need to get the mask every frame, but only every second frame.

### Removing


### On the list (one of these years)

- Webpage that allows you to upload compatible background formats, and manage the app.
- Finish effects. Maybe even extend them to be able to be generated in the webpage?
- Fix the gross compositing code (it fast tho)
   - There is a cleaner_composite() function in image_handler, but its slow and I'm bad at math.

### Ideas

 - SPEED
   - Right now this is sloooow as all heck, python itself is slow so i'm probably fighting an uphill battle here...
   - Maybe rust would be a better idea? Go?
   - Maybe there's a commercial thing?
   - OpenCV can do face recog?
   - Maybe I just remove the bodypix section and use dlib facial landmarks instead?

 - Multiprocessing, Multithreadding, and/or offloading processing to different computers.
   - I have a ton of jetson tk1 boards kicking around, maybe writing a small http server that can recieve an image, mask it (maybe get facial landmarks as well??)

 - Do we just use face_recog to generate the mask instead?
   - We could use the facial landmarks to generate a polygon surrounding the face.
   - Could save some work.


  curl -H "Content-Type: application/json" -X POST --data '{"skip":""}' http://127.0.0.1:9987/

