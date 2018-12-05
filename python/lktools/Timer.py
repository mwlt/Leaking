import time
import lktools.Loader
import lktools.LoggerFactory

settings = lktools.Loader.get_settings()
DEBUG = settings['time_debug']
logger = lktools.LoggerFactory.LoggerFactory('Timer').logger

def timer_decorator(func):
  def wrapper(*args, **kwargs):
    if DEBUG:
      start = time.perf_counter()
    result = func(*args, **kwargs)
    if DEBUG:
      end = time.perf_counter()
      logger.info(f'{func.__name__} time cost: {end - start:.2f}s')
    return result
  return wrapper
