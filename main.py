import pyscreenshot
import time

def main():
  start = time.time()

  while time.time() - start < 10:
    im = pyscreenshot.grab()
    rgb_im = im.convert('RGB')

    l = [ ]
      
    temp = time.time()

    for x in range(400):
      for y in range(900):
        r, g, b = rgb_im.getpixel((x, y))
        l.append((r, g, b))

    print(time.time() - temp)

if __name__ == "__main__":
  main()
