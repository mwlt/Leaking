import shutil
import os
# 读取设置
"""{lk.settings 格式要求:}
path=XXX
videos=X.mp4;Y.mp4
delay=?     // 视频播放延迟，默认100
height=?    // 视频高度限定，宽度会自动计算，默认480
frame_range=a-b// 取a-b帧，默认0-100
img_path=?  // 图片存取路径，默认tmp
video_path=?// 视频存取路径，默认tmp
time_test=? // 是否测试时间，会关闭所有输出，默认false
lastn=?     // 用前N帧图片作为修正的标准，默认为1
fps=?       // 保存视频帧数，默认10
time_debug=?// 是否打印每个函数耗时
limit_size=?// 光流法的参数，默认10
compression_ratio=? // 光流法的压缩率，默认1
linux=?     // 是不是linux，linux不会执行显示相关的函数
"""

settings = None

def get_settings():
  global settings
  if settings is None:
    settings = {}
  else:
    return settings
  with open('lk.settings', encoding='utf-8') as f:
    for line in f.readlines():
      strs = line.split('=')
      settings[strs[0].strip()] = strs[1].strip()
  # 设置
  settings.setdefault('img_path', 'tmp')
  settings.setdefault('video_path', 'tmp')
  settings['delay'] = int(settings.get('delay', 100))
  settings['height'] = int(settings.get('height', 480))
  settings['lastn'] = int(settings.get('lastn', 10))
  settings['fps'] = int(settings.get('fps', 10))
  settings['limit_size'] = int(settings.get('limit_size', 10))
  settings['compression_ratio'] = float(settings.get('compression_ratio', 1))
  settings['frame_range'] = tuple(
    map(lambda s: int(s), settings.get('frame_range', '0-100').split('-'))
  )
  settings['time_test'] = settings.get('time_test') == 'true'
  settings['time_debug'] = settings.get('time_debug') == 'true'
  settings['linux'] = settings.get('linux') == 'true'
  # 将设置中的文件转换为绝对地址
  settings['videos'] = tuple(map(
    lambda n: (n.split('.')[0], '{path}/{name}'.format(
      path=settings['path'],
      name=n
    )),
    settings['videos'].split(';')
  ))
  # 清空输出文件夹
  img_path = settings['img_path']
  if not settings['time_test']:
    if os.path.exists(img_path):
      shutil.rmtree(img_path)
    os.mkdir(img_path)
  video_path = settings['video_path']
  if video_path != img_path:
    if os.path.exists(video_path):
      shutil.rmtree(video_path)
    os.mkdir(video_path)
  return settings
