import grpc
from concurrent import futures
import time
from multiprocessing import cpu_count

# import the generated classes :
import databroker_pb2
import databroker_pb2_grpc

import get_next_row as gnr

PORT = 8061


row_obj = gnr.FetchRowCSV()
current_row = 0

class get_next_rowServicer(databroker_pb2_grpc.get_next_rowServicer):
    #row_obj = gnr.FetchRowCSV()
    
    def get_next_row(self, request, context):
        response = databroker_pb2.Messag()
        total_rows = row_obj.init_count()
        current_row = row_obj.current_row
        print("total number of rows of csv: ", total_rows)

        if current_row == total_rows:
            '''
            This condition is no longer required as the generic orchestrator waits for the status code to terminate an edge
            '''
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('All available data has been processed')
            print("exception raised")
        else:
            row = row_obj.get_next_row(current_row)
            # row = gnr.get_next_row(request.count)
            # row = gnr.get_next_row()
            response.msg = row[0]

            row_obj.current_row = row_obj.current_row + 1

        return response

# creat a grpc server :
server = grpc.server(futures.ThreadPoolExecutor(max_workers=cpu_count()-2))

databroker_pb2_grpc.add_get_next_rowServicer_to_server(get_next_rowServicer(), server)
print("Starting Server. Listening to port :" + str(PORT))
server.add_insecure_port("[::]:{}".format(PORT))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
