import pyscreenshot
from PIL import Image
import time
import numpy
from autopy import mouse

BBOX = (0,0,450,750)
HOOP_COLOR = (255,38,15)
HOOP_ROW = 260

BALL_COLOR = (255,150,47)
BALL_ROW = 670

def main():
  start = time.time()

  while True:
    # get numpy array
    im = numpy.asarray(pyscreenshot.grab(bbox=BBOX))

    # find the hoop location
    hoopcenter = None
    try:
      row = map(tuple, list(im[HOOP_ROW]))
      hoopcenter = get_hoop(row)
    except:
      print 'could not find hoop'

    print hoopcenter

    # find the ball location
    ballcenter = None
    try:
      row = map(tuple, list(im[BALL_ROW]))
      ballcenter = get_ball(row)
    except:
      print 'could not find ball'
    
    print ballcenter

    # drag the mouse
    if ballcenter is not None:
      x1 = hoopcenter
      y1 = HOOP_ROW
      x2 = ballcenter-9
      y2 = BALL_ROW

      mouse.move(x2, y2)
      #time.sleep(0.1)
      for y3 in range(y2+40, y1-40, -1):
        if y3 == y2:
          mouse.toggle(True, 1)
        x3 = int(float(y3-y1)/(y2-y1)*(x2-x1)+x1)
        mouse.move(x3, y3)
        if y3 == y1:
          mouse.toggle(False, 1)
        time.sleep(0.0004)
      time.sleep(2)



def get_ball(row):
  left = row.index(BALL_COLOR)
  right = len(row) - list(reversed(row)).index(BALL_COLOR)
  ballcenter = (left + right) // 2
  return ballcenter

def get_hoop(row):
  left = row.index(HOOP_COLOR)
  right = len(row) - list(reversed(row)).index(HOOP_COLOR)
  hoopcenter = (left + right) // 2
  return hoopcenter

def showImage(array):
    Image.fromarray(array).show()

if __name__ == "__main__":
  main()
