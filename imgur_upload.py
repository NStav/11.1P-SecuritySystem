from auth import authenticate
from datetime import *
import os

def upload_image(client):
    image_time = datetime.now()
    #takes the photo
    os.system('fswebcam -r 1280x720 --no-banner /home/pi/nstavropoulos/images/test.jpg')
    image_path = "/home/pi/nstavropoulos/images/test.jpg"
    
    config = {
        'album': None,
        'name': image_time,
        'title': image_time,
        'description': 'empty'
    }
    
    print("Uploading image")
    image = client.upload_from_path(image_path, config=config, anon=False)
    print("Done")
    print()
    
    #Once the image is uploaded to imgur we delete it from the pi as we don't need it on the pi
    #anymore.
    os.system('rm /home/pi/nstavropoulos/images/test.jpg')
    return image

if __name__ == "__main__":
    client = authenticate()
    image = upload_image(client)
    
    print("Image was posted")
    print("Image URL: {0}".format(image['link']))