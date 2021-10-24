import pickle
import threading
from socket import socket, AF_INET, SOCK_DGRAM, create_server
from bson.json_util import loads
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def mongo_conn(post,mission):

  #Connect to cluster
  client = MongoClient(os.environ.get("client"))

  # Create a database and collection in cluster
  database_main = client.weather_db1
  weather_coll = database_main.weather_coll

  if (mission == 1): # Performs insertion upon datatype from UDP/weather station connection
    weather_coll.insert_one(post)
    print ("Insertion compelete")

  if (mission == 0): # Extract documents from MongoDB based on datatype from TCP/FMI request
    req_data = weather_coll.find(post)
    return req_data


def udp_server():
  sock = socket(AF_INET, SOCK_DGRAM)
  sock.bind(("localhost", 55554))
  mission = 1

  while True:
    msg, addr = sock.recvfrom(2048)
    print(f'{addr[0]} says {msg.decode()}')
    sock.sendto(('ACK: '.encode() + msg), addr) # Will send acknowledgement to the client
    data = eval(msg)
    mongo_conn(data, mission) #Forward data to mongoDB connection

  print ('Insertion complete')


def tcp_server():
    sock = create_server(("localhost", 5550))
    HEADERSIZE = 10
    mission = 0

    while True:
      # now our endpoint knows about the OTHER endpoint.
      conn, address = sock.accept()
      json_req = conn.recv(1024).decode()
      json_req = loads(json_req)

      print(f"Connection from {address} has been established. message: {json_req}")
    
      d = list(mongo_conn(json_req,mission)) # Create list of requested data form mongo_conn

      msg = pickle.dumps(d) #Converts list to string
      msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
      conn.send(msg)


def main():
  # Threading allows multiple processes to run in parallell 
  thread_udp = threading.Thread(target=udp_server)
  thread_tcp = threading.Thread(target=tcp_server)

  thread_udp.start()
  thread_tcp.start()
  
  print('The server is ready to receive TCP/UDP')


if __name__ == '__main__':
    main()
