import numpy as np
import json
import plotly.graph_objs as go
import os
from plotly.subplots import make_subplots

directory_folder = os.getcwd()

# здесь указать название json файла с данными
file_name = '152-12_35_new7p'

with open('result/' + file_name + '.json', 'r') as file:
    data = json.load(file)

# передавать количетво точек? где разрывы и где нет

t = []
x = []
y = []
V = []
Vx = []
Vy = []
A = []
Ax = []
Ay = []
C = []
alpha = []
dR = []
VrR = []
EvR = []
AzR = []


for i in range(len(data["points"])):
    t.append(data["points"][i]["t"])
    x.append(data["points"][i]["x"])
    y.append(data["points"][i]["y"])
    V.append(data["points"][i]["V"])
    Vx.append(data["points"][i]["Vx"])
    Vy.append(data["points"][i]["Vy"])
    A.append(data["points"][i]["A"])
    Ax.append(data["points"][i]["Ax"])
    Ay.append(data["points"][i]["Ay"])
    C.append(data["points"][i]["C"])
    alpha.append(data["points"][i]["alpha"])
    dR.append(data["points"][i]["DistanceR"])
    VrR.append(data["points"][i]["VrR"])
    EvR.append(data["points"][i]["EvR"])
    AzR.append(data["points"][i]["AzR"])

x_fin = data["endpoint_x"]
y_fin = data["endpoint_y"]

# GK


trace_trajectory = go.Scatter(x=x, y=y, name='траектория', mode='markers')
trace_trajectory_fin = go.Scatter(x=[x_fin], y=[y_fin], name='точка падения', mode='markers')

trace_V = go.Scatter(x=t, y=V, name='модуль скорости', mode='markers')
trace_VrR = go.Scatter(x=t, y=VrR, name='радиальная скорость относительно локатора', mode='markers')
trace_Vx = go.Scatter(x=t, y=Vx, name='составляющая по x')
trace_Vy = go.Scatter(x=t, y=Vy, name='составляющая по y')

trace_A = go.Scatter(x=t, y=A, name='модуль ускорения', mode='markers')
trace_Ax = go.Scatter(x=t, y=Ax, name='составляющая по x')
trace_Ay = go.Scatter(x=t, y=Ay, name='составляющая по y')

trace_alpha = go.Scatter(x=t, y=alpha, name='угол наклона - alpha', mode='markers')
trace_EvR = go.Scatter(x=t, y=EvR, name='угол места относительно локатора', mode='markers')

trace_dR = go.Scatter(x=t, y=dR, name='дальность от локатора', mode='markers')

trace_AzR = go.Scatter(x=t, y=AzR, name='азимут локатора', mode='markers')

data1 = [trace_trajectory, trace_trajectory_fin]
data2 = [trace_V, trace_Vx, trace_Vy, trace_VrR]
data3 = [trace_A, trace_Ax, trace_Ay]
data4 = [trace_alpha, trace_EvR]
data5 = [trace_dR]
data6 = [trace_AzR]

# строим графики, хотим вывести один комментируем другие data и rows = 1
fig = make_subplots(rows=6, cols=1)

for x in data1:
    fig.add_trace(x,row=1, col=1)

for x in data2:
    fig.add_trace(x,row=2, col=1)

for x in data3:
    fig.add_trace(x,row=3, col=1)
#
for x in data4:
    fig.add_trace(x,row=4, col=1)

for x in data5:
    fig.add_trace(x,row=5, col=1)

for x in data6:
    fig.add_trace(x,row=6, col=1)

fig.update_layout(title_text="Графики файла " + file_name)

fig.update_traces(hoverinfo="all", hovertemplate="x: %{x}<br>y: %{y}")

# вывести в браузер или созранить
#fig.show(renderer="browser")
fig.write_html('result/' + file_name + '.html')
# добавлять в название