FROM ubuntu:20.04

LABEL maintainer=rluque@catec.aero

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip

RUN pip3 install numpy
RUN pip3 install pandas

WORKDIR /
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

# RUN useradd app
# USER app
COPY LICENSE databroker.proto csv_server.py get_next_row.py test.csv ./
COPY . /

RUN python3 -m grpc_tools.protoc --python_out=. --proto_path=. --grpc_python_out=. *.proto
# RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. *.proto

ENTRYPOINT [ "python3","-u","csv_server.py" ]
# CMD python3 csv_server.py
