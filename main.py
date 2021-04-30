import socket
import json
import time
import plotly.graph_objs as go



HEADER = 64
PORT = 5050
SERVER = '192.168.43.43'
ADDR = (SERVER, PORT)


mes = {}
mes["loc_B"] = 56.28861111111111
mes["loc_L"] = 43.083825000000004
mes["loc_H"] = 0.
mes["can_B"] = 56.28884722222222
mes["can_L"] = 43.083825000000004
mes["can_H"] = 2.
mes["alpha"] = 45.
mes["az"] = 0.
mes["hei"] = 0.
mes["wind_module"] = 0.
mes["wind_direction"] = 0.
mes["bullet_type"] = 3
mes["temperature"] = 20
mes["atm_pressure"] = 798

meas = []
f = open('82_17-02.txt', 'r')
for line in f:

    a = line.split()
    poit = {}
    poit["execTime_sec"] = float(a[1])
    poit["Beta"] = 0.
    poit["sBeta"] = 0.
    poit["Epsilon"] = float(a[5])
    poit["sEpsilon"] = 0.
    poit["R"] = float(a[3])
    poit["sR"] = 0.
    poit["Vr"] = float(a[4])
    poit["sVr"] = 0.
    poit["Amp"] = float(a[2])
    meas.append(poit)

f.close()

meas_dict = {}
meas_dict["meas"] = meas

print(meas_dict)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen()
print("Waiting")
conn, addr = server.accept()
print("[NEW CONNECTION]")
while True:
    data1 = input()
    if data1 == "1":
        data2send = json.dumps(mes).encode()
        conn.sendall(len(data2send).to_bytes(4, "little"))
        conn.sendall((0x150001).to_bytes(4, "little"))
        conn.sendall(data2send)
    elif data1 == "2":
        t0 = time.time()
        data2send = json.dumps(meas_dict).encode()
        print(len(data2send))
        data = json.loads(data2send.decode())
        print(data)
        conn.sendall(len(data2send).to_bytes(4, "little"))
        conn.sendall((0x150002).to_bytes(4, "little"))
        conn.sendall(data2send)

        while True:

            rcv_size = int.from_bytes(conn.recv(4), "little")
            rcv_type = int.from_bytes(conn.recv(4), "little")

            print("Size {}".format(rcv_size))
            print("Type {:0x}".format(rcv_type))

            data = conn.recv(rcv_size)
            last_bytes = rcv_size - len(data)

            while last_bytes > 0:
                data = data + conn.recv(last_bytes)
                last_bytes = rcv_size - len(data)

            if rcv_type == 0x150003:
                data = json.loads((data.decode()))
                print(data, "track config")
                print(time.time() - t0, "время обработки в секундах")

                t = []
                Vx = []
                Vh = []
                V = []

                VrR = []

                for i in range(len(data["points"])):
                    t.append(data["points"][i]["t"])
                    Vx.append(data["points"][i]["Vx"])
                    Vh.append(data["points"][i]["Vy"])
                    V.append(data["points"][i]["V"])
                    VrR.append(data["points"][i]["VrR"])


                fig = go.Figure()

                fig.add_trace(go.Scatter(x=t, y=V, name=('V')))
                fig.add_trace(go.Scatter(x=t, y=Vx, name=('Vx')))
                fig.add_trace(go.Scatter(x=t, y=Vh, name=('Vy')))
                fig.add_trace(go.Scatter(x=t, y=VrR, name=('VrR')))

                fig.update_layout(legend_orientation="h",
                                  legend=dict(x=.5, xanchor="center"),
                                  hovermode='x',
                                  title_text='Скорости',
                                  xaxis_title="t, c",
                                  yaxis_title="v, м")

                fig.update_traces(hoverinfo="all", hovertemplate="x: %{x}<br>y: %{y}")
                fig.show(renderer="browser")






