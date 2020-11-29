from PIL import Image
import os
import requests
import time
# converts the image into a square and converts RGBA to RGB
def make_square(im, min_size=0):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), "WHITE")
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)), im)
    return new_im

# uses remove.bg call to remove background from image. Return RGBA image.
def remove_background(image_path):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(image_path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': 'hcM54vWhAtKudf4pXvyhCvRR'},
    )
    if response.status_code == requests.codes.ok:
        with open(image_path, 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)

# function to resize an image and convert RGBA to RGB. Contains flags to execute other functions.
def resize_image(dir_path, image_name, image_size=(127, 127), square=False, remove_bg=False):
    image_path = os.path.join(dir_path, image_name)
    if remove_bg:
        remove_background(image_path)
    im = Image.open(image_path)
    if square:
        im = make_square(im)
    im = im.convert("RGB", palette=Image.ADAPTIVE)
    im = im.resize(image_size)
    im.save(image_path)

# main function to execute
def inference(dir_path):
	imagelist = [file for file in os.listdir(dir_path) if file.endswith('.png')]

	# resize and remove background for all images
	for image in imagelist:
		resize_image(dir_path, image, square=True, remove_bg=True)
		time.sleep(0.5)