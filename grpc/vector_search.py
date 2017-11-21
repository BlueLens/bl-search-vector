# coding: utf-8
from __future__ import absolute_import

import numpy as np
import os
import faiss
from bluelens_log import Logging

INDEX_FILE = os.environ['INDEX_FILE']
REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='bl-search-vector')

class SearchVector(object):
  def __init__(self):
    try:
      self.index = faiss.read_index(INDEX_FILE)
      log.info('Init')
    except Exception as e:
      log.error(str(e))

  def search(self, vector):
    log.info('search')
    xq = np.expand_dims(np.array(vector, dtype=np.float32), axis=0)

    xq.astype(np.float32)
    result_d, result_i = self.index.search(xq, 10)
    log.debug(result_i)
    log.debug(result_d)
    log.debug(result_i)
    return np.squeeze(result_i)


