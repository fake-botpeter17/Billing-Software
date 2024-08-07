from app import app
from waitress import serve
from socket import socket 
import socket as socket_

def find_open_socket(): 
    s = socket(socket_.AF_INET, socket_.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

application = app

if __name__ == '__main__':
    port = find_open_socket()
    print(f"Starting server on port {port} and listening on all IP")
    serve(app=application,port=port,host='0.0.0.0')