from time import sleep
from os import system
from picamera import PiCamera


camera = PiCamera()
camera.resolution = (1024, 768)
camera.rotation = -90

# Prime the camera 
print('starting timelapse')
camera.start_preview()
sleep(3)

for i in range(60):
    camera.capture('testgif/image{0:04d}.jpg'.format(i))
    print('image index{} captured'.format(i))
    sleep(10)

print('starting conversion')
system('convert testgif/image*.jpg animation.gif')
print('done')
