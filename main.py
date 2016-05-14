import pyscreenshot
from PIL import Image
import time
import numpy

BBOX = (0,0,450,750)
TARGET_COLOR = (255,38,15)
TARGET_ROW = 260

BALL_COLOR = (255,150,47)
BALL_ROW = 670

def main():
  start = time.time()

  while True:
    # get numpy array
    im = numpy.asarray(pyscreenshot.grab(bbox=BBOX))
    # this is the target location
    row = map(tuple, list(im[TARGET_ROW]))
    hoopcenter = get_hoop(row)

    for t in im[BALL_ROW]:
      print t

    showImage(im[BALL_ROW:BALL_ROW+20])

    print hoopcenter
    break

def get_hoop(row):
  try:
    left = row.index(TARGET_COLOR)
    right = len(row) - list(reversed(row)).index(TARGET_COLOR)
    hoopcenter = (left + right) // 2
    return hoopcenter
  except:
    return "could not find hoop"

def showImage(array):
    Image.fromarray(array).show()

if __name__ == "__main__":
  main()
