import pandas as pd
import numpy as np
import cv2

class memStore:

  store = {}
  maxCam = 4

  def __init__(self, name):
    self.add(name)

  def add(self, name):
    if name not in memStore.store:
      memStore.store[name] = {}
      memStore.store[name]['name'] = name
      memStore.store[name]['targets']  = pd.DataFrame(columns=['plugin'])
      memStore.store[name]['frameIn']  = []
      memStore.store[name]['frameOut'] = []
      for i in range(memStore.maxCam):
        img = self.create_blank(600,100)
        memStore.store[name]['frameIn'].append(img)
        memStore.store[name]['frameOut'].append(img.copy())
  
  def updateFrameIn(self, name, cam, frameIn):
    if name in memStore.store:
      if cam < memStore.maxCam:
        memStore.store[name]['frameIn'][cam] = frameIn
    else:
      self.add(name)
      if cam < memStore.maxCam:
        memStore.store[name]['frameIn'][cam] = frameIn

  def updateFrameOut(self, name, cam, frameOut):
    if name in memStore.store:
      if cam < memStore.maxCam:
        memStore.store[name]['frameOut'][cam] = frameOut
    else:
      self.add(name)
      if cam < memStore.maxCam:
        memStore.store[name]['frameOut'][cam] = frameIn

  def updateTargets(self, name, targets):
    if name in memStore.store:
      memStore.store[name]['targets']  = targets

  def fetch(self, name):
    if name in memStore.store:
      return memStore.store[name]
    return {}

  def fetchTargets(self, name):
    if name in memStore.store:
      return memStore.store[name]['targets']
    return {}

  def fetchFrameIn(self, name, camera=0):
    if name in memStore.store:
      camera = int(camera)
      if camera < len(memStore.store[name]['frameIn']):
        return memStore.store[name]['frameIn'][camera]
    return self.create_blank(600,100)

  def fetchFrameOut(self, name, camera=0):
    if name in memStore.store:
      camera = int(camera)
      if camera < len(memStore.store[name]['frameOut']):
        return memStore.store[name]['frameOut'][camera]
    return self.create_blank(600,100)

  def print(self):
    for s in memStore.store:
      print(memStore.store[s]['name'])

  def create_blank(self, width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    cv2.putText(image, "ERROR check image source!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255,255,255), 3)
    return image

if __name__ == "__main__":
  
  targets  = pd.DataFrame(columns=['plugin'])
  frameIn  = []
  frameOut = []
  frameIn.append(255 * np.ones(shape=[512, 512, 3], dtype=np.uint8))
  frameOut.append(255 * np.ones(shape=[512, 512, 3], dtype=np.uint8))

  ms = memStore('Camera')
  ms.add('Mask')
  ms.add('Model')

  o = ms.fetch('Calc')

  ms.print()
