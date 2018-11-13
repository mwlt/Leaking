# 读取设置
"""{rpca.settings 格式要求:}
path=XXX
videos=X.mp4;Y.mp4
delay=?     // 视频播放延迟，默认100
height=?    // 视频高度限定，宽度会自动计算，默认192
frame_range=a-b// 取a-b帧，默认0-100
img_path=?  // 图片存取路径，默认tmp/
video_path=?  // 图片存取路径，默认saveVideo.avi
time_test=? // 是否测试时间，会关闭所有输出，默认false
lastn=?     // 用前N帧图片作为修正的标准，默认为1
"""

def get_settings():
  settings = {}
  with open('rpca.settings', encoding='utf-8') as f:
    for line in f.readlines():
      strs = line.split('=')
      settings[strs[0].strip()] = strs[1].strip()
  # 设置
  settings.setdefault('img_path', 'tmp/')
  settings.setdefault('video_path', 'saveVideo.avi')
  settings['delay'] = int(settings.get('delay', 100))
  settings['height'] = int(settings.get('height', 192))
  settings['lastn'] = int(settings.get('lastn', 1))
  settings['frame_range'] = tuple(
    map(lambda s: int(s), settings.get('frame_range', '0-100').split('-'))
  )
  settings['time_test'] = settings.get('time_test') == 'true'
  # 将设置中的文件转换为绝对地址
  settings['videos'] = tuple(map(
    lambda n: (n, '{path}/{name}'.format(
      path=settings['path'],
      name=n
    )),
    settings['videos'].split(';')
  ))
  return settings