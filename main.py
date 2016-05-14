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

    # find the hoop location
    try:
      row = map(tuple, list(im[TARGET_ROW]))
      hoopcenter = get_hoop(row)
    except:
      print 'could not find hoop'
      continue

    print hoopcenter

    # find the ball location
    try:
      row = map(tuple, list(im[BALL_ROW]))
      ballcenter = get_ball(row)
    except:
      print 'could not find ball'
      continue
    
    print ballcenter
    print


def get_ball(row):
  left = row.index(BALL_COLOR)
  right = len(row) - list(reversed(row)).index(BALL_COLOR)
  ballcenter = (left + right) // 2
  return ballcenter

def get_hoop(row):
  left = row.index(TARGET_COLOR)
  right = len(row) - list(reversed(row)).index(TARGET_COLOR)
  hoopcenter = (left + right) // 2
  return hoopcenter

def showImage(array):
    Image.fromarray(array).show()

if __name__ == "__main__":
  main()
