from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from helper_utils import BasicControl, BasicSensor


#### SETUP DASH APP ####
external_stylesheets = [dbc.themes.BOOTSTRAP, "../assets/style.css", 
                        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "BL 5.3.1"
app._favicon = 'LBL_icon.ico'

# Placeholder for control API
beamline = 'als_5_3_1'
version = '0'
controls_url = f'http://beamline_control:8080/api/v0/beamline/{beamline}/{version}'

# Manually defining the controls for now
MONO_CONTROL = BasicControl(prefix="IOC:m1", name="Mono theta [deg]", id="mono", min=0, max=100, units='°')
MONO_CONTROL.connect()

LONG_CONTROL = BasicControl(prefix="IOC:m3", name="Longitudinal stage [deg]", id="long", min=0, max=100, units='°')
LONG_CONTROL.connect()

CURRENT_SENSOR = BasicSensor(prefix="Bl201-beamstop:current", name="Current sensor", id="current", units="\u03BCA")
CURRENT_SENSOR.create_gui()

CONTROL_LIST = [MONO_CONTROL, LONG_CONTROL, CURRENT_SENSOR]
CONTROL_GUI = MONO_CONTROL.gui_comp + LONG_CONTROL.gui_comp + CURRENT_SENSOR.gui_comp


### BEGIN DASH CODE ###
# APP HEADER
HEADER = dbc.Navbar(
            dbc.Container([
                dbc.Row([
                    dbc.Col(
                        html.Img(id="app-logo",
                                 src="assets/LBL_logo.png",
                                 height="60px"),
                        md="auto"
                    ),
                    dbc.Col(
                        html.Div(
                            id = 'app-title',
                            children=[html.H3("Advanced Light Source | Beamline 5.3.1")],
                        ),
                        md=True,
                        align="center",
                    )
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.NavbarToggler(id="navbar-toggler"),
                        html.Div(
                            dbc.Nav([
                                dbc.NavItem(
                                    dbc.Button(className="fa fa-github",
                                               style={"font-size": 40, "margin-right": "1rem", "color": "#00313C", "background-color": "white"},
                                               href="https://github.com/als-computing/beamline531")
                                               ),
                                dbc.NavItem(
                                    dbc.Button(className="fa fa-question-circle-o",
                                               style={"font-size": 40, "color": "#00313C", "background-color": "white"},
                                               href="https://github.com/als-computing/beamline531")
                                               )
                            ],
                            navbar=True)
                        )
                    ])
                ])
            ],
            fluid=True),
        dark=True,
        color="#00313C",
        sticky="top"
        )


# BEAMLINE INPUTS (CONTROLS)
BL_INPUT = html.Div(id='bl-controls',
                    children=CONTROL_GUI)


# BEAMLINE OUTPUTS (SCANS, CAMERAS, ETC)
BL_OUTPUT = [dbc.Card(
                children=[
                    dbc.CardHeader("Camera"),
                    dbc.CardBody(html.Div(id='bl-camera'))
                    ]
                ),
             dbc.Card(
                children=[
                    dbc.CardHeader("Scan"),
                    dbc.CardBody(html.Div(id='bl-scan',
                                          children=[
                                            dbc.Row(
                                                html.Img()
                                            ),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label('Minimum', style={'textAlign': 'center'}),
                                                    dbc.Input()
                                                ]),
                                                dbc.Col([
                                                    dbc.Label('Step', style={'textAlign': 'center'}),
                                                    dbc.Input()
                                                ]),
                                                dbc.Col([
                                                    dbc.Label('Maximum', style={'textAlign': 'center'}),
                                                    dbc.Input()
                                                ]),
                                                dbc.Col(
                                                    dbc.Button('GO',
                                                               color="success",
                                                               style={'width': '100%'}),
                                                    align="end"
                                                ),
                                                dbc.Col(
                                                    dbc.Button('ABORT',
                                                               color="danger",
                                                               style={'width': '100%'}),
                                                    align="end"
                                                )
                                           ])
                                          ]))
                    ]
                )
            ]


##### DEFINE LAYOUT #####
app.layout = html.Div(
    [
        HEADER,
        dbc.Container([
                dbc.Row([
                    dbc.Col(BL_INPUT, width=4),
                    dbc.Col(BL_OUTPUT, width=8),
                ]),
                dcc.Interval(id='refresh-interval')],   # time interval to refresh the app, default 1000 milliseconds
                fluid=True
                ),
    ]
)
