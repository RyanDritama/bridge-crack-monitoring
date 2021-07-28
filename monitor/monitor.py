import dash_core_components as dcc
import dash_html_components as html
import dpd_components as dpd
import numpy as np
import plotly.graph_objects as go

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from dash.dependencies import Input, Output
from dash_table import Format, DataTable
from django_plotly_dash import DjangoDash
from scipy import interpolate
import monitor.database as db
import plotly.express as px


info = [
    "Sensor failed to measue bridge's health.",
    "Out of service - beyond corrective action. Replacement required.",
    "Major deterioration or section loss present in critical structural components or obvious vertical or horizontal movement affecting structure stability Rehabilitation or Replacement required.",
    "Advanced deterioration of primary stuctural elements.Fatigue cracks in steel or shear cracks in concrete may be present or scour may have removed substucture support. Rehabilitation or Replacement required.",
    "Loss of section, deterioration spalling or scour have seriously affected primary structural components. Local failure are possible. Fatigue cracks in steel or shear cracks may present Rehabilitation or Replacement required",
    "Primary structural elements are sound but may have some minor problems. Preventive Maintenance and/or Repairs required",
    "Structural elements show some minor deterioration. Preventive Maintenance and/or Repairs required",
    "There are some minor problems. The Bridge needs Preventive Maintenance",
    "There are some minor problems. The Bridge needs Preventive Maintenance",
    "The Bridge needs Preventive Maintenance",
]

condition = [
    "FAILED MEASUREMENT. ",
    "FAILED CONDITION. ",
    "IMMINENT FAILURE CONDITION. ",
    "CRITICAL CONDITION. ",
    "SERIOUS CONDITION. ",
    "FAIR CONDITION. ",
    "SATISFACTORY CONDITION. ",
    "GOOD CONDITION. ",
    "VERY GOOD CONDITION. ",
    "EXCELLENT CONDITION. "
]

crack_location = [
    "",
    "There is a crack in area 1 with center x=1 and y=2 on the bridge",
    "There is a crack in area 2 with center x=2 and y=2 on the bridge",
    "There is a crack in area 3 with center x=3 and y=2 on the bridge",
    "There is a crack in area 4 with center x=4 and y=2 on the bridge",
    "There is a crack in area 5 with center x=4 and y=1 on the bridge",
    "There is a crack in area 6 with center x=3 and y=1 on the bridge",
    "There is a crack in area 7 with center x=2 and y=1 on the bridge",
    "There is a crack in area 8 with center x=1 and y=1 on the bridge",
]

sensor_funct = [
    "All Sensors work fine",
    "Sensor 1 failed to process data!",
    "Sensor 2 failed to process data!",
    "Sensor 3 failed to process data!",
    "Sensor 4 failed to process data!",
    "Sensor 5 failed to process data!",
    "Sensor 6 failed to process data!",    
    "Sensor 7 failed to process data!",
    "Sensor 8 failed to process data!",
    "Sensor 9 failed to process data!",
    "Sensor 10 failed to process data!"
]

dummy=[[0, 0, 0.22, 0], [0, 0.5, 0, 0]]


history = db.getData(50, 1)
dd_table = DjangoDash('PartTable')

if len(history) != 0:
    col = [{"name": i, "id": i} for i in history[0].keys()]
else:
    #For testing, database is empty so we must
    #fill the column manually
    col = [{"name": i, "id": i} for i in range(14)]


col[0]["name"] = "date UTC+7\n(yyyy-MM-dd hh:mm:ss)"

col[1]["name"] = "health\nindex"

col[2]["name"] = "mean freq.\n(Hz)"
col[2]["type"] =  'numeric'
col[2]["format"] = Format.Format(
    precision=3,
)

col[3]["name"] = "ideal freq.\n(Hz)"
col[3]["type"] =  'numeric'
col[3]["format"] = Format.Format(
    precision=3,
)

for i in range(4,14):
    col[i]["name"] = "amplitude" + str(i-2) +  u"\n(m/s\u00b2)"
    col[i]["type"] =  'numeric'
    col[i]["format"] = Format.Format(
        precision=3,
    )
dd_table.layout = html.Div(children=[
    html.Div(children= DataTable(
        id='PartTable',
        columns=col,
        data=history,
        style_cell={
            'whiteSpace': 'pre',
            'textAlign': 'center',
        },
        sort_action="native",
        row_selectable="single",
    )),
])

dd_surface3d = DjangoDash('SimpleExample')
dd_surface3d.layout = html.Div(children=[
    dcc.Graph(
        id="3dgraph",
        figure=go.Figure(go.Surface())
    )
])


dd_interface2D = DjangoDash('SimpleExample2')
dd_interface2D.layout = html.Div(children=[
    dcc.Graph(
        id="2dgraph",
        figure=px.imshow(dummy)
    )
])


dd_monitor = DjangoDash('monitor',add_bootstrap_links=True)
dd_monitor.layout = html.Div(children=[
    # First row
    html.Div(children=[
        html.Div(children=[
            html.Div('Choose Bridge:',style={'margin-top':'5px'}),
            ],className='col-md-fluid'
        ),
        html.Div(children=[
            dcc.Dropdown(
                id='dropdown',
                options=db.get_bridges_dropdown(),
                value=1
            ),],className='col-md'
        ),
    ],className='row'),

    #Second row
    html.Div(children=[
        #First column
        html.Div(children=[
            dd_table.layout
            ],className='col-md-8'
            ,style={'height':'800px','overflowY':'scroll'}
        ),

        #Second column
        html.Div(children=[
            #Nested row
            html.Div(children=[
                html.P("Latest Health Index:",style={'font-size':'150%','margin-bottom':'0px'}),
                html.P(style={'font-size':'400%','font-weight': 'bold','margin-bottom':'0px'},id='idx'),
                html.P(condition[0],style={'font-size':'150%','margin-bottom':'10px'},id='condition'),
                html.P(info[0],style={'font-size':'120%'},id='info'),
            ],className='row-12',style={'background':'blue'},id='bgi'),
            html.Div(children=[
                dd_interface2D.layout,
            ],className='row-12', style={'overflowX': 'auto'}),
            html.Div(children=[
                html.P(crack_location[0],style={'font-size':'100%','margin-bottom':'0px'},id='cracks'),
            ],className='row-12',style={'overflowX': 'auto'}),
            html.Div(children=[
                html.P(sensor_funct[0],style={'font-size':'100%','margin-bottom':'10px'},id='sensorx'),
            ],className='row-12',style={'overflowX': 'auto'}),
            html.Div(children=[
                dd_surface3d.layout,
            ],className='row-12', style={'overflowX': 'auto'}),
        ],className='col-md-4 text-center'),
    ],className='row'),

    # Auxiliary
    # pylint: disable=no-member
    dpd.Pipe(
        id="updater_pipe",
        label="updater",
        channel_name="updater_channel"
    ),
    html.Div(id='dummy', style={'display':'none'}),
],className='container-fluid')

def update3D(data):
    """data is a dict of 10 mode shapes"""
    z = np.array([
        [data.get('mode_shape1'), data.get('mode_shape6')],
        [data.get('mode_shape2'), data.get('mode_shape7')],
        [data.get('mode_shape3'), data.get('mode_shape8')],
        [data.get('mode_shape4'), data.get('mode_shape9')],
        [data.get('mode_shape5'), data.get('mode_shape10')]
    ])
    xmin = ymin = 1
    xmax , ymax = 5, 2
    x = np.linspace(xmin,xmax,xmax)
    y = np.linspace(ymin,ymax,ymax)


    dx, dy = 50,10
    x_i = np.linspace(xmin,xmax,dx)
    y_i = np.linspace(ymin,ymax,dy)
    # f = interpolate.RectBivariateSpline(x,y,z,ky=ymax-1)
    # z_i = f(x_i,y_i)

    f = interpolate.interp2d(y,x,z)
    z_i = f(y_i,x_i)

    fig = go.Figure(go.Surface(x = y_i,y = x_i,z = z_i,colorscale ='dense'))
    fig.update_layout(
        autosize=False,
#        colorscale="Viridis",
        scene_aspectmode='manual',
        scene_aspectratio=dict(y=2.5,x=1,z=0.5),
        scene = dict(
            xaxis = dict(nticks=2,),
            yaxis = dict(nticks=5,),
            zaxis_title="Amplitude"+u"\n(m/s\u00b2)",
        ),
        margin=dict(l=0, r=0, b=00, t=30),
        scene_camera= dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=-0.5),
            eye=dict(x=1.75, y=1.75, z=1.75)
        ),
        title="Fundamental amplitude plot:",
    )
    return fig

def update2D(data):
    """data is a dict of 10 mode shapes"""
    z = np.array([[data.get('value8'), data.get('value7'), data.get('value6'), data.get('value5')],
                  [data.get('value1'), data.get('value2'), data.get('value3'), data.get('value4')]
        ])

    fig = px.imshow(z, labels=dict(color="Bridge Crack"),
                x=['1', '2', '3', '4'],
                y=['1', '2'], range_color=[0,1],color_continuous_scale = px.colors.sequential.Bluered
               )

    fig.update_layout(
                      xaxis_title = "coordinate x",
                      yaxis_title = "coordinate y",
                      autosize=False,
                      width=450,
                      height=450,
                      title="Bridge Crack Detection:",

    )
    return fig

def sensor_notification(data):

    z = np.array([
        data.get('status1'), data.get('status2'),
        data.get('status3'), data.get('status4'),
        data.get('status5'), data.get('status6'),
        data.get('status7'), data.get('status8'),
        data.get('status9'), data.get('status10')
    ])

    notifikasi = "Status : "
    count = 0
    for i in range(10):
        if z[i] == 0.0:
            count = count+1
            notifikasi = notifikasi + sensor_funct[i+1] + "\n"
    
    if count == 0:
        notifikasi = notifikasi + sensor_funct[0]
    return notifikasi

def crack_notification(data):

    z = np.array([
        data.get('bridge_crack1'), data.get('bridge_crack2'),
        data.get('bridge_crack3'), data.get('bridge_crack4'),
        data.get('bridge_crack5'), data.get('bridge_crack6'),
        data.get('bridge_crack7'), data.get('bridge_crack8')
    ])
    indeks = 0
    for i in range(8):
        if z[i] == "1":
            indeks = i+1
    return(indeks)


@dd_monitor.callback(
    [Output('PartTable', 'data'),
    Output('3dgraph', 'figure'),
    Output('idx', 'children'),
    Output('info', 'children'),
    Output('condition', 'children'),
    Output('bgi', 'style'),
    Output('dropdown', 'options'),
    Output('2dgraph', 'figure'),
    Output('sensorx', 'children'),
    Output('cracks', 'children')],
    [Input('updater_pipe', 'value'),
    Input('dropdown', 'value'),
    Input('PartTable', "selected_rows")]
)
def update_poutput(u_value, d_value, lvalue):
    """update callback of main monitor page"""
    history_ = db.getData(50, d_value)
    history_value = db.getValue(50, d_value)
    history_sensor = db.getSensor(50, d_value)
    history_cracks = db.getCracks(50, d_value)
    test_notification = "Status : "
    if history_:
        latest = history_[0]
        latest_value = history_value[0]
        latest_sensor = history_sensor[0]
        latest_cracks = history_cracks[0]
        test_notification = ""
        if lvalue is None:
            fig = update3D(latest)
            fig2 = update2D(latest_value)
            test_notification = sensor_notification(latest_sensor)
            crack_indeks = crack_notification(latest_cracks)
        else:
            fig = update3D(history_[lvalue[0]])
            fig2 = update2D(history_value[lvalue[0]])
            test_notification = sensor_notification(history_sensor[lvalue[0]])
            crack_indeks = crack_notification(history_cracks[lvalue[0]])
        indeks = latest.get('health_index')
        if indeks < 5:
            color = 'red'
        else:
            color = 'green'
        return [history_, fig, indeks, info[indeks], condition[indeks],{'background':color},
            db.get_bridges_dropdown(), fig2,test_notification,crack_location[crack_indeks]]
    else:
        fig = go.Figure()
        fig.update_layout(
            autosize=False,
            margin=dict(l=0, r=0, b=00, t=30),
            scene_camera= dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=-0.5),
                eye=dict(x=1.75, y=1.75, z=1.75)
            ),
            title="Fundamental amplitude plot:",
        )
        fig2 = px.imshow(dummy,
            labels=dict(x="coordinate x", y="coordinate y", color="Bridge Crack"),
            x=['1', '2', '3', '4'],
            y=['1', '2'], range_color=[0,1]
            )
        return [history_, fig, -1, "Empty database.", "",{'background':'red'},
            db.get_bridges_dropdown(), fig2, "", ""]


class Monitor(LoginRequiredMixin, TemplateView):
    """Monitor page view"""
    template_name = 'monitor.html'
    login_url = 'login'
