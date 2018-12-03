# import
import numpy as np
import cv2
import lktools
# load
settings = lktools.Loader.get_settings()
time_test = settings['time_test']
img_path = settings['img_path']
video_path = settings['video_path']
frame_range = settings['frame_range']
lastn_interval = settings['lastn']
fps = settings['fps']
limit_size = settings['limit_size']
compression_ratio = settings['compression_ratio']
delay = settings['delay']
linux = settings['linux']
OF = settings['OF']
sift = settings['sift']
@lktools.Timer.timer_decorator
def catch_abnormal(lastn, last, src, fgbg, size):
  """
  对一帧图像进行处理，找到异常就用框圈出来。

  Args:
    lastn:  前N帧图片，用于对齐
    last:   上一帧图片，用于光流法寻找移动物体
    src:    原图，用于画框，并显示
    fgbg:   BackgroundSubtractionMOG2方法使用的一个类
    size:   图片尺寸，生成框使用

  Returns:
    src_rects:  画上了框的原图
  """
  frame = src
  # rect
  rect = lktools.PreProcess.get_rect_property(size) 
  # optical flow
  if OF:
    flow_rects, _ = lktools.OpticalFlow.optical_flow_rects(
      last, frame, rect,
      limit_size=limit_size, compression_ratio=compression_ratio
    )
  # sift alignment
  if sift:
    frame, *_ = lktools.SIFT.siftImageAlignment(lastn, frame)
  # MOG2 BS
  frame = fgbg.apply(frame)
  # Denoise
  frame = lktools.Denoise.denoise(frame, 'bilater')
  frame = lktools.Denoise.denoise(frame, 'morph_open')
  frame = lktools.Denoise.denoise(frame, 'dilation')
  frame = lktools.Denoise.denoise(frame, 'dilation')
  frame = lktools.Denoise.denoise(frame, 'erode') 
  # findObject
  bs_rects = lktools.FindObject.findObject(frame, rect)
  # draw
  src_rects = src.copy()
  cv2.rectangle(src_rects, *rect)
  # rects
  rects = bs_rects
  if OF:
    rects.extend(flow_rects)
  for rect in rects:
    cv2.rectangle(src_rects, *rect)
  return src_rects
# 计时运行
@lktools.Timer.timer_decorator
def run(name, path):
  capture, h, w, fps = lktools.PreProcess.video_capture_size(path, settings['height'])
  size = (w, h)
  # run
  print(f'read {path}. from frame {frame_range[0]} to {frame_range[1]}')
  nframes = 0
  # init
  last = None
  lastn = None
  fgbg = cv2.createBackgroundSubtractorMOG2()
  # 将图像保存为视频
  if not time_test:
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWriter = cv2.VideoWriter(
      f'{video_path}/{name}.avi',
      fourcc,
      fps,
      size # WARNING：尺寸必须与图片的尺寸一致，否则保存后无法播放。
    )
  # 对每一帧
  while capture.isOpened():
    if nframes >= frame_range[1]:
      break
    success, frame = capture.read()
    if not success:
      break
    nframes += 1
    if nframes < frame_range[0]:
      continue
    frame = cv2.resize(frame, size)
    if last is None:
      last = frame
      lastn = frame
      continue
    # 上面是循环变量，下面是正式计算
    # 保存原图
    original = frame
    frame = catch_abnormal(lastn, last, frame, fgbg, size)
    if time_test:
      cv2.imshow(f'{name}', frame)
      cv2.waitKey(delay)
    else:
      cv2.imwrite(
        f'{img_path}/{name}_{nframes}.jpg',
        frame
      )
      # 每一帧导入保存的视频中，uint8
      videoWriter.write(np.uint8(frame))
    # 更新last
    if nframes % lastn_interval == 0:
      lastn = original
      fgbg = cv2.createBackgroundSubtractorMOG2()
      fgbg.apply(lastn)
    last = original
  capture.release()
  # 导出视频
  if not time_test:
    videoWriter.release()
  if not linux:
    cv2.destroyAllWindows()
# run
if __name__ == '__main__':
  for name, video in settings['videos']:
    run(name, video)
