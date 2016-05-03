import cv2
import re

class BackgroundSubtractor(object):
  """Wraps OpenCV's background subtractor"""
  def __init__(self, history, threshold, detectShadows):
    self.history = history
    self.threshold = threshold
    self.detectShadows = detectShadows

    version = int(re.findall(r'\d+', cv2.__version__)[0])
    if version == 3:
      self.operator = cv2.createBackgroundSubtractorMOG2(self.history,
        self.threshold, self.detectShadows)
    elif version == 2:
      self.operator = cv2.BackgroundSubtractorMOG2(self.history,
        self.threshold, self.detectShadows)
    else:
      raise Exception("Unsupported OpenCV version {0}".format(version))

  def model_bg2(self, video, N=100):
      vidcapture = cv2.VideoCapture(video)
      # Initialize from first N frames
      for _ in range(N):
          ret, frame = vidcapture.read()
          if ret:
              self.operator.apply(frame)
          else:
              break
      vidcapture.release()

  def apply(self, *args, **kwargs):
    return self.operator.apply(*args, learningRate=-1, **kwargs)
