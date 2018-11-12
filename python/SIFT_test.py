# import
import numpy as np
import cv2
import os
import shutil
import lktools
# load
settings = lktools.Loader.get_settings()
time_test = settings['time_test']
img_path = settings['img_path']
frame_range = settings['frame_range']
lastn_interval = settings['lastn']
def run_one_frame(normal, src, fgbg):
  # sift alignment
  sift_save = None
  if normal is None:
    sift = src
  else:
    sift, *_ = lktools.SIFT.siftImageAlignment(normal, src)
    sift_save = sift
  # MOG2 BS
  sift = fgbg.apply(sift)
  # Denoise
  if normal is None:
    return cv2.cvtColor(sift, cv2.COLOR_GRAY2RGB)
  else:
    sifts = lktools.Denoise.denoise(sift)
    # to rgb
    sifts = map(lambda img: cv2.cvtColor(img, cv2.COLOR_GRAY2RGB), sifts)
    #
    return tuple(sifts), sift_save
# 计时运行
@lktools.Timer.timer_decorator
def run(name, path):
  capture, h, w = lktools.PreProcess.video_capture_size(path, settings['height'])
  # run
  print('read {path}'.format(path=path))
  nframes = 0
  # init
  first = None
  lastn = None
  fgbg_first = cv2.createBackgroundSubtractorMOG2()
  if not time_test:
    fgbg_lastn = cv2.createBackgroundSubtractorMOG2()
    fgbg = cv2.createBackgroundSubtractorMOG2()
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
    frame = cv2.resize(frame, (w, h))
    if first is None:
      first = frame
      lastn = frame
      continue
    if not time_test:
    if not time_test:
      siftimg_last, *_ = SIFT.siftImageAlignment(last, frame)
      sift_frame_last = sift_fgbg_last.apply(siftimg_last)
      sift_frame_last = cv2.cvtColor(sift_frame_last, cv2.COLOR_GRAY2RGB)
      frame = fgbg.apply(frame)
      frame_lastn, sift_lastn = run_one_frame(lastn, frame, fgbg_lastn)
      frame = run_one_frame(None, frame, fgbg)
      line1 = np.hstack((
        original, frame,
        sift_first, frame_first[0],
        sift_lastn, frame_lastn[0]
      ))
      line2 = np.hstack((
        np.zeros(original.shape),
        frame_first[1], frame_first[2],
        frame_first[3], frame_first[3],
        np.zeros(original.shape),
      ))
      cv2.imwrite(
        '{path}/{name}_{n}.jpg'.format(
          path=img_path, name=name, n=nframes
        ),
        np.vstack((line1, line2))
      )
    # 更新last
    if nframes % lastn_interval == 0:
      lastn = original
  capture.release()
  cv2.destroyAllWindows()

def main():
  # 清空输出文件夹
  if not time_test:
    if os.path.exists(img_path):
      shutil.rmtree(img_path)
    os.mkdir(img_path)
  for name, video in settings['videos']:
    run(name.split('.')[0], video)
# run
if __name__ == '__main__':
  main()