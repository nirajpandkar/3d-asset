import os
import io
import uuid
import numpy as np
import cv2
import subprocess
import sys
import traceback

from PIL import Image
from flask import Flask, render_template, request, flash
from helper import inference

sys.path.insert(0, './3D-R2N2/')
from demo import infer
from lib.config import cfg_from_list
print("IMPORTED DEMO")

app = Flask(__name__)

app.config['UPLOAD_FOLDER_VIDEOS'] = 'static/uploaded_videos'
app.config['PROCESSED_IMAGES'] = 'static/processed_images'

app.config['SECRET_KEY'] = 'averyverysecretkeythatnoonewouldguess'

def convert_bytes_to_image(img_bytes):
    """Convert bytes to numpy array
    Args:
        img_bytes (bytes): Image bytes read from flask.
    Returns:
        [numpy array]: Image numpy array
    """
    
    pil_image = Image.open(io.BytesIO(img_bytes))
    if pil_image.mode=="RGBA":
        image = Image.new("RGB", pil_image.size, (255,255,255))
        image.paste(pil_image, mask=pil_image.split()[3])
    else:
        image = pil_image.convert('RGB')
    
    image = np.array(image)
    
    return image

def get_length(input_video):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/image', methods=['GET', 'POST'])
def get_image():
    if request.method == 'POST':
        try:
            if request.files.get('video'):
                video = request.files["video"]
                uid = str(uuid.uuid4())[:8]
                filename = uid + ".mp4"
                original_video_path = os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], filename)
                video.save(original_video_path)

                video_duration = get_length(original_video_path)
                
                # Make separate folder using the unique id
                unique_folder = os.path.join(app.config['PROCESSED_IMAGES'], uid)
                os.system("mkdir -p " + unique_folder)
                os.system("ffmpeg -i {} -r {} -start_number 0 {}/%01d.png".format(original_video_path, 0.5, unique_folder))
                print("Done extracting frames")

                imagelist = [file for file in os.listdir(unique_folder) if file.endswith('.png')]
                num_imgs = len(imagelist)

                # Resize and infer
                inference(unique_folder)
                print("Done resizing images")
                
                # Running inference from demo.py
                cfg_from_list(['CONST.BATCH_SIZE', 1])
                infer(num_imgs, unique_folder)
                print("Inference done!")

                return render_template('index.html', original_video_path=original_video_path)
        except:
            flash("Our server hiccuped :/ Please upload another file! :)")
            print(traceback.format_exc())
            return render_template('index.html')
    else:
        return render_template("index.html")

@app.route('/asset')
def create_asset():
    return render_template("index.html")

if __name__ == "__main__":
    app.run("0.0.0.0", 8000, debug=True, use_reloader=False)
