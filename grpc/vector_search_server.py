# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from concurrent import futures
import time

import grpc
import os
import numpy as np

from vector_search import SearchVector
import vector_search_pb2
import vector_search_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Search(vector_search_pb2_grpc.SearchServicer):
  def __init__(self):
    self.vc = SearchVector()

  def SearchVector(self, request, context):
    v_d, v_i = self.vc.search(request.vector)
    return vector_search_pb2.SearchReply(vector_d=np.array(v_d).tobytes(), vector_i=np.array(v_i).tobytes())


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=50))
  vector_search_pb2_grpc.add_SearchServicer_to_server(Search(), server)
  server.add_insecure_port('[::]:50054')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
