import grpc
from random import randint
from timeit import default_timer as timer

# import the generated classes
import model_pb2
import model_pb2_grpc

start_ch = timer()
port_addr = 'localhost:8061'

# open a gRPC channel
channel = grpc.insecure_channel(port_addr)

# create a stub (client)
stub = model_pb2_grpc.CopyStub(channel)

end_ch = timer()
msg_list   = ["hello1", "hello2", "hello3"]
ans_lst = []
start = timer()

for i in range(0,len(msg_list)):
    # create a valid request message
    requestCopy  = model_pb2.Messag(msg = msg_list[i])
    
    # make the call
    responseCopy = stub.copy_message(requestCopy)
    ans_lst.append(responseCopy.msg)
    print('The Copy is :',responseCopy.msg)

print('Done!')
end = timer()
all_time = end - start
ch_time = end_ch - start_ch

print ('Time spent for {} copying is {}'.format(len(msg_list),(all_time)))
print('In average, {} second for each copy'.format(all_time/len(msg_list)))
print('That means you can do {} copies in one second'.format(int(1/(all_time/len(msg_list)))))
print('Time for connecting to server = {}'.format(ch_time))