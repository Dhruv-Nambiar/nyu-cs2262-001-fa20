from flask import Flask, request
import socket
app = Flask(__name__)

def fib(n):
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

@app.route('/fibonacci')
def fibonacci():
    if "number" not in request.args:
        return '', 400
    number_str = request.args.get("number")
    try:
        number = int(number_str)
    except:
        return '', 400
    return str(fib(number)), 200

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    print("FS Received JSON:", data, flush=True)
    fields = ['hostname', 'ip', 'as_ip', 'as_port']
    for field in fields :
        if field not in data:
            return 'Bad Registration Request', 400
    hostname = data['hostname']
    ip = data['ip']
    as_ip = data['as_ip']
    as_port = int(data['as_port'])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"TYPE=A\nNAME={hostname} VALUE={ip} TTL=10\n"
    print("Sending registration...", flush=True)
    sock.sendto(message.encode(), (as_ip, as_port))
    print(f"Dest: {as_ip}, {as_port}", flush=True)  
    data, addr = sock.recvfrom(4096)
    message = data.decode()
    print("Reply: ", message, flush=True)  
    return 'Registered!\n', 201

app.run(host='0.0.0.0',
        port=9090,
        debug=True,
        use_reloader=False)
