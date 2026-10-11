import socket, threading, collections, time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

HOST, PORT = "0.0.0.0", 8002
N = 200
xs, ys, zs = (collections.deque([0]*N, maxlen=N) for _ in range(3))
state = {"last_event": 0.0, "count": 0}

def server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT)); s.listen(1)
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
            line = line.strip()
            if line.startswith("EVENT"):
                state["last_event"] = time.time()
                state["count"] += 1
                print(time.strftime("%H:%M:%S"), ">>> SIGNIFICANT MOTION DETECTED")
                continue
            try:
                x, y, z = map(int, line.split(","))
                xs.append(x); ys.append(y); zs.append(z)
            except ValueError:
                pass
    print("disconnected")

threading.Thread(target=server, daemon=True).start()

fig, ax = plt.subplots()
lx, = ax.plot(list(xs), label="X")
ly, = ax.plot(list(ys), label="Y")
lz, = ax.plot(list(zs), label="Z")
ax.set_ylim(-2200, 2200)
ax.set_ylabel("Acceleration (mg)")
ax.legend(loc="upper right")
banner = ax.text(0.5, 0.92, "", transform=ax.transAxes, ha="center",
                 fontsize=16, fontweight="bold", color="red")

def update(_):
    lx.set_ydata(list(xs)); ly.set_ydata(list(ys)); lz.set_ydata(list(zs))
    if time.time() - state["last_event"] < 3:
        banner.set_text("Significant Motion Detected!")
        fig.patch.set_facecolor("#ffe0e0")
    else:
        banner.set_text("")
        fig.patch.set_facecolor("white")
    ax.set_title(f"LSM6DSL Accelerometer  (events: {state['count']})")
    return lx, ly, lz, banner

ani = animation.FuncAnimation(fig, update, interval=100, blit=False)
plt.show()