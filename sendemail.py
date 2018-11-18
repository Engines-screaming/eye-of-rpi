# Python script to send email of picture from raspberry pi

# Import libraries for python camera
from time import sleep
from picamera import PiCamera

# First import the needed libraries
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib

# Import creds from config
from secrets import MY_ADDRESS, PASSWORD

def send_email(to_addr, sub, img_attachment):
    # Compose email in MIME format.
    # We want to send an email with a message and png attachment
    msg = MIMEMultipart()
    msg["Subject"] = sub
    msg["To"] = to_addr
    msg["From"] = MY_ADDRESS 

    # Attaching img to email
    with open(img_attachment, "rb") as f:
        mime_img= MIMEImage(f.read())
        msg.attach(mime_img)

    # Try sending, and print if it goes wrong
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com")
        server.login(MY_ADDRESS, PASSWORD)
        server.sendmail(MY_ADDRESS, to_addr, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(e)
        print("Email not sent!")


def take_picture(filename):
    # Create a PiCamera object to control the pi's camera
    camera = PiCamera()

    # We want to rotate the photo since the camera is upside down
    camera.rotation = 180

    camera.start_preview()
    sleep(5)
    camera.capture(filename)
    print("Picture Taken!")
    

def main():
    # First define where you want to send and subject
    TARGET_ADDRESS = "karl.ravago@gmail.com" #Replace this with recipient
    SUBJECT = "Stove Query" 
    IMG = "stove.png"

    # Take the picture
    take_picture(IMG)

    send_email(TARGET_ADDRESS, SUBJECT, IMG)


if __name__ == "__main__":
    main()
