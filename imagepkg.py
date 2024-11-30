import math
from urllib.request import urlopen
from PIL import Image
import random
from cmu_graphics import *


def loadAndResizeCMUImageLocal(path, resizeFactor):
    PILImageFull = Image.open(path)
    fullWidth, fullHeight = PILImageFull.size
    width, height = fullWidth//resizeFactor, fullHeight//resizeFactor
    image = PILImageFull.resize((width, height))
    CMUImageReturn = CMUImage(image)
    return CMUImageReturn, width, height 

def loadPILImageLocal(path):
    PILImageFull = Image.open(path)
    return PILImageFull

#This function was taken from the PIL demo through the 15-112 website:
def loadPilImageURL(url):
    # Loads a PIL image (not a CMU image!) from a url:
    return Image.open(urlopen(url))