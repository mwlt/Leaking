import cv2
from lktools import PreProcess

def findObject(img, rect):
  # 计算图像中目标的轮廓并且返回彩色图像
  _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
  _, contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
  #
  rects = []
  for c in contours:
    # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
    if cv2.contourArea(c) < 20:
      continue
    (x, y, w, h) = cv2.boundingRect(c) # 该函数计算矩形的边界框
    if not PreProcess.in_rect((x, y), rect):
      continue
    rects.append(((x, y), (x + w, y + h), (0, 0, 255), 2))
  return rects