from multiprocessing import Process
from concurrent import futures
import time

import grpc
import os
import signal
import sys
import redis
import numpy as np

from vector_search import SearchVector
import vector_search_pb2
import vector_search_pb2_grpc
from bluelens_log import Logging


REDIS_SEARCH_RESTART_QUEUE = 'bl:search:restart:queue'
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
GRPC_PORT = os.environ['GRPC_PORT']

rconn = redis.StrictRedis(REDIS_SERVER, port=6379, password=REDIS_PASSWORD)
options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='bl-search-vector')

class Search(vector_search_pb2_grpc.SearchServicer):
  def __init__(self):
    self.vc = SearchVector()

  def SearchVector(self, request, context):
    v_d, v_i = self.vc.search(request.vector)
    return vector_search_pb2.SearchReply(vector_d=np.array(v_d).tobytes(), vector_i=np.array(v_i).tobytes())


def serve(rconn):
  log.info('Start serve')
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=50))
  vector_search_pb2_grpc.add_SearchServicer_to_server(Search(), server)
  server.add_insecure_port('[::]:' + GRPC_PORT)
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

def restart(rconn, pids):
  while True:
    key, value = rconn.blpop([REDIS_SEARCH_RESTART_QUEUE])
    log.info('Restart serve')
    for pid in pids:
      os.kill(pid, signal.SIGTERM)
    sys.exit()

if __name__ == '__main__':
  pids = []
  p1 = Process(target=serve, args=(rconn,))
  p1.start()
  pids.append(p1.pid)
  Process(target=restart, args=(rconn, pids)).start()
