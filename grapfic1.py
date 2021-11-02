import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
import matplotlib.pyplot as plt
#pio.renderers.default = 'svg'


import os

directory_folder = os.getcwd()

file_name = 'trackdata_bullet'

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


trace_R = go.Scatter(x=t, y=R, name='расстояние', mode='markers')
trace_Vr = go.Scatter(x=t, y=Vr, name='радиальная скорость относительно локатора', mode='markers')
trace_E = go.Scatter(x=t, y=E, name='угол', mode='markers')

fig = make_subplots(rows=3, cols=1)

fig.add_trace(trace_R, row=1, col=1)
fig.add_trace(trace_Vr, row=2, col=1)
fig.add_trace(trace_E, row=3, col=1)


fig.update_traces(hoverinfo="all", hovertemplate="x: %{x}<br>y: %{y}")

fig.write_html('result/12.html')
# добавлять в название

# применение фильтра для угла
# def func_angle_smoother(theta_meas, t_meas):
#     # Rauch-Thug-Striebel algorithm
#     x_est_prev = np.array([theta_meas[0], 0.004])
#     dx_est_prev = np.eye(2)
#
#     sigma_ksi = 4e-2
#     D_ksi = sigma_ksi ** 2
#     I = np.eye(2)
#
#     H = np.array([1,0])
#     sigma_n = 5e-4
#     Dn = sigma_n ** 2
#
#     dT = 0
#     for i in range(len(theta_meas)):
#         if i == 0:
#             dT = 0.05
#         else:
#             dT = t_meas[i] - t_meas[i-1]
#
#         F = np.array([[1, dT], [0, 1]])
#         G = np.array([[0, 0], [0, dT]])
#
#         x_ext = F.dot(x_est_prev)
#         dx_ext = F.dot(dx_est_prev).dot(F.T)
#         s = H.dot(dx_ext).dot(H.T) + Dn
#         k = dx_ext.dot(H.T).dot(np.linalg.inv(s))
#         x_est_prev = x_ext + k.dot(theta_meas[k] - H.dot(x_ext))
#         dx_est_prev = (I - k.dot(H)).dot(dx_ext)
#


# применение фильтра для координаты и скорости
