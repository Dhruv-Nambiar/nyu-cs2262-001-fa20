import socket
import os

# os.makedirs("DNS_INFO", exist_ok=True)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 53533))
dns_map = dict()
print("Starting to listen", flush=True)
while True:
    data, addr = sock.recvfrom(4096)
    print(f"AS Received: {addr}: {data.decode()}", flush=True)
    message = data.decode()

    # filename = f"{SAVE_DIR}/from_{addr[0]}_{addr[1]}.txt"
    # with open(filename, "w") as f:
        # f.write(data.decode())
    line = message.split('\n')[1].split(' ')
    if len(line) == 1:
        name = line[0].split('=')[1]
        ip = dns_map[name]
        print(line, name)
        reply = f"TYPE=A\nNAME={name} VALUE={ip} TTL=10\n"
        sock.sendto(reply.encode(), addr)
    else:
        # Registration
        name = line[0].split('=')[1]
        ip = line[1].split('=')[1]
        dns_map[name] = ip
        print(f"DNS_map: {dns_map}", flush=True)
        reply = f"Registration Successful!\n"
        sock.sendto(reply.encode(), addr)