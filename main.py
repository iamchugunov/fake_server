import socket
import json
import time
import plotly.graph_objs as go
import os

directory_folder = os.getcwd()

HEADER = 64
PORT = 5050
SERVER = '192.168.1.8'
ADDR = (SERVER, PORT)


mes = {}
mes["loc_B"] = 56.28913
mes["loc_L"] = 43.083811400000002
mes["loc_H"] = 100.
mes["can_B"] = 56.289346700000003
mes["can_L"] = 43.083765
mes["can_H"] = 98.
mes["alpha"] = 5.
mes["az"] = 0.
mes["hei"] = 0.
mes["wind_module"] = 240.
mes["wind_direction"] = 2.
mes["bullet_type"] = 2

mes["temperature"] = 5
mes["atm_pressure"] = 752

points = []
file_name = '152-14-46-1'
f = open(file_name + '.txt', 'r')


# for line in f:
# # определить и договориться как именно по строкам считывать файлы с измерениями
#     a = line.split()
#     poit = {}
#     poit["execTime"] = float(a[1])
#     poit["Beta"] = 0.
#     poit["sBeta"] = 0.
#     poit["Epsilon"] = float(a[5])
#     poit["sEpsilon"] = 0.
#     poit["R"] = float(a[3])
#     poit["sR"] = 0.
#     poit["Vr"] = float(a[4])
#     poit["sVr"] = 0.
#     poit["Amp"] = float(a[2])
#     points.append(poit)

# for line in f:
# # определить и договориться как именно по строкам считывать файлы с измерениями
#     a = line.split()
#     poit = {}
#     poit["execTime"] = float(a[0])
#     poit["Beta"] = 0.
#     poit["sBeta"] = 0.
#     poit["Epsilon"] = float(a[5])
#     poit["sEpsilon"] = 0.
#     poit["R"] = float(a[1])
#     poit["sR"] = 0.
#     poit["Vr"] = float(a[2])
#     poit["sVr"] = 0.
#     poit["Amp"] = 0
#     poit["az"] = float(a[4])
#     points.append(poit)

# for line in f:
#
#     a = line.split()
#     poit = {}
#     poit["execTime"] = float(a[1])
#     poit["Beta"] = 0.
#     poit["sBeta"] = 0.
#     poit["Epsilon"] = float(a[6])
#     poit["sEpsilon"] = 0.
#     poit["R"] = float(a[3])
#     poit["sR"] = 0.
#     poit["Vr"] = float(a[4])
#     poit["sVr"] = 0.
#     poit["Amp"] = float(a[2])
#     points.append(poit)
#
f.close()

meas_dict = {}
meas_dict["points"] = points

file_name = 'trackdata_762'
with open(file_name + '.json', 'r') as file:
    data = json.load(file)

meas_dict = {}
meas_dict["points"] = data["points"]

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
                print(time.time() - t0, "время обработки в секундах")

                with open('result/' + file_name + '.json', "w", encoding="utf-8") as file:
                    json.dump(data, file)

                print('Выполнено')

            if rcv_type == 0x150004:
                data = json.loads((data.decode()))
                print(time.time() - t0, "время обработки в секундах")

                with open('result/' + file_name + '.json', "w", encoding="utf-8") as file:
                    json.dump(data, file)

                print('Выполнено c ошибкой')









