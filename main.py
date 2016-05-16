import pyscreenshot
from PIL import Image
import time
import numpy
from autopy import mouse
import sys

BBOX = (0,0,450,750)
HOOP_COLOR = (255,38,15)
HOOP_RIM_COLOR = (183,183,183)
HOOP_ROW = 260
HOOP_WIDTH = 253
HOOP_CENTER = 215

BALL_COLOR = (255,150,47)
BALL_ROW = 670

SCREEN_WIDTH = 500
HOOP_PERIOD = 3.74  # round-trip, seconds

def main(lvl):
  start = time.time()

  last_hoop = None
  hoopcenter = None

  ballcenter = None
  last_ball = None

  if lvl is None:
    lvl = 0

  while True:
    print '========='
    print 'level', lvl

    # get numpy array
    im = numpy.asarray(pyscreenshot.grab(bbox=BBOX))

    # find the hoop location
    last_hoop = hoopcenter
    try:
      hoopcenter = get_hoop(im, HOOP_ROW)
    except:
      print 'could not find hoop'

    print 'hoop', hoopcenter

    # find the ball location
    last_ball = ballcenter
    ballcenter = None
    try:
      row = map(tuple, list(im[BALL_ROW]))
      ballcenter = get_ball(row)
    except:
      print 'could not find ball'
    
    print 'ball', ballcenter

    if hoopcenter is None or last_hoop is None or ballcenter is None:
      continue

    print 'diff', abs(hoopcenter-ballcenter)

    # drag the mouse
    if ballcenter is not None:
      if lvl < 10:
        # levels 1-10
        x1 = hoopcenter
        y1 = HOOP_ROW
        x2 = ballcenter-9
        y2 = BALL_ROW
        launch_ball(x2, y2, x1, y1)
        lvl += 1

      elif lvl < 20:
        # levels 10+
        if abs(last_hoop-ballcenter) > abs(hoopcenter-ballcenter) and 100 < abs(hoopcenter-ballcenter) < 140:
          launch_ball(ballcenter, BALL_ROW, ballcenter, HOOP_ROW)
          lvl += 1

      else:
        if abs(last_hoop-ballcenter) > abs(hoopcenter-ballcenter) and 100 < abs(hoopcenter-ballcenter) < 120:
          time.sleep(0.77 * HOOP_PERIOD)
          launch_ball(ballcenter, BALL_ROW, ballcenter, HOOP_ROW)
          lvl += 1


def launch_ball(x0, y0, x1, y1):
  mouse.move(x0, y0)
  #time.sleep(0.1)
  for y3 in range(y0+40, y1-40, -1):
    if y3 == y0:
      mouse.toggle(True, 1)
    x3 = int(float(y3-y1)/(y0-y1)*(x0-x1)+x1)
    if y3 % 10 == 0:
      mouse.move(x3, y3)
    if y3 == y1:
      mouse.toggle(False, 1)
    time.sleep(0.001)
  time.sleep(1)





def get_ball(row):
  left = row.index(BALL_COLOR)
  right = len(row) - list(reversed(row)).index(BALL_COLOR)
  ballcenter = (left + right) // 2
  return ballcenter

def get_hoop(img, rowNum):
  row = map(tuple, list(img[rowNum]))
  edges = []
  prev = None
  grayCount = 0
  for x in range(len(row)):
    if prev == HOOP_RIM_COLOR and row[x] == HOOP_RIM_COLOR:
      grayCount += 1
    else:
      grayCount = 0
    if grayCount > 50:
      return None
    if row[x] == HOOP_RIM_COLOR and prev != HOOP_RIM_COLOR:
      edges.append(x)
    prev = row[x]
  print 'edges', edges

  # one edge - figure out if it's the left or right edge
  if len(edges) == 1:
    colNum = edges[0]
    while tuple(img[rowNum][colNum]) == HOOP_RIM_COLOR:
      rowNum += 1
    rowNum -= 1
    dCol = 0
    while True:
      dCol += 1
      # hit right
      if tuple(img[rowNum][colNum+dCol]) != HOOP_RIM_COLOR:
        return colNum - HOOP_WIDTH // 2
      # hit left
      if tuple(img[rowNum][colNum-dCol]) != HOOP_RIM_COLOR:
        return colNum + HOOP_WIDTH // 2

  # two edges - take the average
  elif len(edges) == 2:
    return sum(edges) // 2

  # three edges - figure out if you're on the left or right
  elif len(edges) == 3:
    leftdX = abs(edges[0])
    rightdX = abs(edges[2] - SCREEN_WIDTH)
    if leftdX < rightdX:
      return sum(edges[:2]) // 2
    else:
      return sum(edges[1:]) // 2

  # four edges - take the average
  elif len(edges) == 4:
    return sum(edges[1:3]) // 2
  
  # nothing found
  return None

def showImage(array):
    Image.fromarray(array).show()

if __name__ == "__main__":
  if len(sys.argv) == 2:
    main(sys.argv[1])
  else:
    main(None)
