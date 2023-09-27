import base64
import glob
import random
import uuid
from locust import task, events, FastHttpUser, between

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--images-folder", type=str, env_var="IMAGES_FOLDER", default="inputfolder", help="The folder with input images.")


class MobileUser(FastHttpUser):
    wait_time = between(1, 10)
    images = []

    @task
    def detect_object(self):
        # Get random image from the images folder
        image = random.choice(self.images)
        
        # Generate UUID for image
        id = uuid.uuid5(uuid.NAMESPACE_OID, image)

        payload = {}
        payload['id'] = str(id)

        # Encode image into base64 string and it to payload
        with open (image, 'rb') as image_file:
            payload['image'] =  base64.b64encode(image_file.read()).decode('utf-8')

        with self.rest(method="POST", url="/object_detection", json=payload) as resp:
            if resp.js is None:
                print(f"An error occurred: : {resp.status_code}.")
                pass # No need to do anything, already marked as failed
            elif 'id' not in resp.js or 'objects' not in resp.js:
                resp.failure(f"'id' or 'objects' missing from response {resp.text}.")
            elif resp.js['id'] != payload['id']:
                resp.failure(f"'id' had an unexpected value: {resp.js['id']}.")
    
    def on_start(self):
        for image_file in glob.iglob(f"{self.environment.parsed_options.images_folder}/*.jpg"):
            self.images.append(image_file)
