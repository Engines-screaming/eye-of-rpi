from time import sleep
from os import system
from picamera import PiCamera
import cv2
import numpy as np


def create_time_lapse(directory):
    '''Creates a timelapse and saves all pictures to
    a directory of choice'''

    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.rotation = -90

    # Prime the camera 
    print('starting timelapse')
    camera.start_preview()
    sleep(3)

    for i in range(60):
        camera.capture(directory + '/image{0:04d}.jpg'.format(i))
        print('image index{} captured'.format(i))
        sleep(1)

def lapse_dir2gif(lapse_path, save_path):
    '''Takes all images saved in special format: image{0:04d}
    and converts to gif'''
    print('starting conversion')
    system('convert ' + lapse_path + '/image*.jpg '+ save_path)
    print('done')


def add_icon(target_pic, source_icon, picture_path):
    ''' Function adds source icon on target picture
    and saves to target path'''

    img1 = cv2.imread(target_pic)
    img2 = cv2.imread(source_icon)

    # Define area of icon for mask and placement
    rows, cols, channels = img2.shape
    roi = img1[0:rows, 0:cols] # area of img where image will be placed

    # Convert the icon to greyscale to make a mask and inv mask
    img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Threshold, since its a black bg,
    # we need the icon to be white to get the fg,
    # and invert the mask to get the background of img1
    ret, mask = cv2.threshold(img2gray, 90, 255, cv2.THRESH_BINARY) 
    mask_inv = cv2.bitwise_not(mask)

    # Get the fg of icon and bg of img
    fg = cv2.bitwise_and(img2, img2, mask=mask)
    bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    added = cv2.add(fg, bg)

    # Set the roi equal to the result
    img1[0:rows, 0:cols] = added

    cv2.imwrite(picture_path, img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    '''Create timelapse, add image, create gif'''

    icon = 'empire.png'
    with_icon_path = r'withimage'

    # Create timelapse and save to testgif folder
    create_time_lapse('/testgif')

    # Add icon
    for i in os.listdir('./testgif'):
        add_icon(r'/testgif/' + i, icon, r'/withimage/' + i)

    # Convert images in folder to gif
    lapse_dir2gif(r'/withimage', 'added_lapse.gif')


if __name__ == '__main__':
    main()
