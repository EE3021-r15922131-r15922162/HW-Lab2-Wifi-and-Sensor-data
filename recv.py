import socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 8002)); s.listen(1)
print("waiting")
c, a = s.accept()
print("connected", a)
buf = ""
while True:
    d = c.recv(1024)
    if not d: break
    buf += d.decode(errors="ignore")
    while "\n" in buf:
        line, buf = buf.split("\n", 1)
        print(line)