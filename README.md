# 3d-asset

> Generates a 3D object file using a 2D video camera input. 

## Dependencies
- System
  - Ubuntu 18.04
  - GPU - Tesla T4
  - Cuda 10.0
  - Cudnn 7.6.5
- Python 3.6
  - Flask==1.1.2
  - numpy==1.18.5
  - opencv-python==4.4.0.42
  - Pillow==7.2.0
  - requests==2.25.0
  - pygpu
- ffmpeg 
- ffprobe

## Installation
1. To make the portable Anaconda environment use the following command - 
```
conda create -n py3-theano python=3.6
source activate py3-theano
```

2. Install the python dependencies. Most of the dependencies are bundled into a requirements file.
```
conda install pygpu
conda install -c anaconda cudnn
pip install -r requirements.txt
```

3. In case you don't have the extra system dependencies - 
```
sudo apt-get install ffmpeg ffprobe
```

## Usage
To run the webapp, you'll need to run the entrypoint python application - 
```
python app.py
```

Now you can navigate to `localhost:8000/image` to interact with the demo. The inference does take time (around 1 and a half minute at max).

## License
MIT 2020
