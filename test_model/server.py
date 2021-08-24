import grpc
from concurrent import futures
import time
from multiprocessing import cpu_count

# import the generated classes :
import model_pb2
import model_pb2_grpc

import utils 

PORT = 8061

# create a class to define the server functions, derived from
class TestServicer(model_pb2_grpc.CopyServicer):
    
    def copy_message(self, request, context): #same name as rpc service in model.proto
        # define the buffer of the response :
        response = model_pb2.Messag()
        # get the value of the response by calling the desired function :
        response.msg = request.msg + "world"
        print(response.msg)
        return response


# creat a grpc server :
server = grpc.server(futures.ThreadPoolExecutor(max_workers = cpu_count()-2))
model_pb2_grpc.add_CopyServicer_to_server(TestServicer(), server)

print("Starting server. Listening on port : " + str(PORT))
server.add_insecure_port("[::]:{}".format(PORT))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
