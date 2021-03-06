# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import vector_search_pb2 as vector__search__pb2


class SearchStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SearchVector = channel.unary_unary(
        '/searchvector.Search/SearchVector',
        request_serializer=vector__search__pb2.SearchRequest.SerializeToString,
        response_deserializer=vector__search__pb2.SearchReply.FromString,
        )


class SearchServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def SearchVector(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SearchServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SearchVector': grpc.unary_unary_rpc_method_handler(
          servicer.SearchVector,
          request_deserializer=vector__search__pb2.SearchRequest.FromString,
          response_serializer=vector__search__pb2.SearchReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'searchvector.Search', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
