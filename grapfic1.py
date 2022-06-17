import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
import numpy as np
import matplotlib.pyplot as plt
#pio.renderers.default = 'svg'


import os

directory_folder = os.getcwd()

#file_name = 'new_logs/trackdata11'
file_name = 'new_logs/trackdata_mina'

with open(file_name + '.json', 'r') as file:
    data = json.load(file)

# передавать количетво точек? где разрывы и где нет
points = data['points']

meas_dict = {}
meas_dict["points"] = points

t = []
R = []
Vr = []
E = []


for i in range(len(meas_dict["points"])):
    t.append(meas_dict["points"][i]["execTime"])
    R.append(meas_dict["points"][i]["R"])
    Vr.append(meas_dict["points"][i]["Vr"])
    E.append(meas_dict["points"][i]["Epsilon"])

text = []
text.append(t)
text.append(R)
text.append(Vr)
text.append(E)

t = np.array(t)
R = np.array(R)
Vr = -(np.array(Vr))
E = np.array(E)

trace_R = go.Scatter(x=t, y=R, name='расстояние измерения', mode='markers')
trace_Vr = go.Scatter(x=t, y=Vr, name='радиальная скорость относительно локатора измерения', mode='markers')
trace_E = go.Scatter(x=t, y=E, name='угол измерения', mode='markers')
#
fig = make_subplots(rows=3, cols=1)

fig.add_trace(trace_R, row=1, col=1)
fig.add_trace(trace_Vr, row=2, col=1)
fig.add_trace(trace_E, row=3, col=1)

fig.update_traces(hoverinfo="all", hovertemplate="x: %{x}<br>y: %{y}")

fig.write_html('result/new_logs/mina.html')

# здесь указать название json файла с данными
#file_name = 'new_logs/trackdata11'
file_name = 'new_logs/trackdata_mina'

with open('result/' + file_name + '.json', 'r') as file:
    data = json.load(file)

# передавать количетво точек? где разрывы и где нет

t = []
x = []
y = []

Vx = []
Vy = []

Ax = []
Ay = []


dR = []
VrR = []
EvR = []


for i in range(len(data["points"])):
    t.append(data["points"][str(i)]["t"])
    x.append(data["points"][str(i)]["x"])
    y.append(data["points"][str(i)]["y"])

    Vx.append(data["points"][str(i)]["Vx"])
    Vy.append(data["points"][str(i)]["Vy"])

    Ax.append(data["points"][str(i)]["Ax"])
    Ay.append(data["points"][str(i)]["Ay"])

    dR.append(data["points"][str(i)]["DistanceR"])
    VrR.append(data["points"][str(i)]["VrR"])
    EvR.append(np.rad2deg(data["points"][str(i)]["EvR"]))

trace_trajectory = go.Scatter(x=x, y=y, name='траектория', mode='markers')

trace_dR = go.Scatter(x=t, y=dR, name='дальность от локатора', mode='markers')
trace_EvR = go.Scatter(x=t, y=EvR, name='угол места относительно локатора', mode='markers')

trace_VrR = go.Scatter(x=t, y=VrR, name='радиальная скорость относительно локатора', mode='markers')


trace_Vx = go.Scatter(x=t, y=Vx, name='скорость составляющая по x')
trace_Vy = go.Scatter(x=t, y=Vy, name='скорость составляющая по y')


trace_Ax = go.Scatter(x=t, y=Ax, name='ускорение составляющая по x')
trace_Ay = go.Scatter(x=t, y=Ay, name='ускорение составляющая по y')
data1 = [trace_trajectory]
data2 = [trace_R, trace_dR]
data3 = [trace_Vr, trace_VrR]

data4 = [trace_E, trace_EvR]

data5 = [ trace_Vx, trace_Vy]
data6 = [trace_Ax, trace_Ay]

fig = make_subplots(rows=6, cols=1)

for x in data1:
    fig.add_trace(x,row=1, col=1)

for x in data2:
    fig.add_trace(x,row=2, col=1)

for x in data3:
    fig.add_trace(x,row=3, col=1)

for x in data4:
    fig.add_trace(x,row=4, col=1)
for x in data5:
    fig.add_trace(x,row=5, col=1)
for x in data6:
    fig.add_trace(x, row=6, col=1)






# fig = make_subplots(rows=2, cols=1)
# for x in data5:
#     fig.add_trace(x,row=1, col=1)
# for x in data6:
#     fig.add_trace(x, row=2, col=1)


fig.update_traces(hoverinfo="all", hovertemplate="x: %{x}<br>y: %{y}")

fig.write_html('result/new_logs/trackdata_mina_res.html')
#
# fig.update_traces(hoverinfo="all", hovertemplate="x: %{x}<br>y: %{y}")
#
# fig.write_html('result/new_logs/trackresult_long_dr_0.html')

