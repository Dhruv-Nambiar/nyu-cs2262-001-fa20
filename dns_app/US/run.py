from flask import Flask, request
import socket
import requests
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/fibonacci')
def print_time():
    fields = ['hostname', 'fs_port', 'number', 'as_ip', 'as_port']
    for field in fields: 
        if field not in request.args:
            return 'Bad Request', 400
    
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = int(request.args.get("as_port"))

    # Query DNS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"TYPE=A\nNAME={hostname}\n"
    print(f"Dest: {as_ip}, {as_port}", flush=True)
    sock.sendto(message.encode(), (as_ip, as_port))  
    data, addr = sock.recvfrom(4096)
    message = data.decode()
    print("DNS Query Response: ", message, flush=True)

    fs_ip = message.split('\n')[1].split(' ')[1].split('=')[1]
    
    url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
    response = requests.get(url)
    return response.text, response.status_code

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
