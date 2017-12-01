# coding: utf-8
from __future__ import absolute_import

import numpy as np
import os
from util import s3
import faiss
from bluelens_log import Logging

AWS_BUCKET = 'bluelens-style-index'
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
INDEX_FILE = os.environ['INDEX_FILE']
REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='bl-search-vector')
storage = s3.S3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)

class SearchVector(object):
  def __init__(self):
    log.info('Init')
    try:
      file = self.load_index_file()
      self.index = faiss.read_index(file)
    except Exception as e:
      log.error(str(e))

  def load_index_file(self):
    log.info('load_index_file')
    file = os.path.join(os.getcwd(), INDEX_FILE)
    try:
      return storage.download_file_from_bucket(AWS_BUCKET, file, INDEX_FILE)
    except:
      log.error('download error')
      return None

  def search(self, vector):
    log.info('search')
    xq = np.expand_dims(np.frombuffer(vector, dtype=np.float32), axis=0)

    xq.astype(np.float32)
    result_d, result_i = self.index.search(xq, 10)
    log.debug(result_d)
    log.debug(result_i)
    return np.squeeze(result_d), np.squeeze(result_i)
