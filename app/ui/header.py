from turtle import width
from config import strings
from dash import dcc,html
import dash_bootstrap_components as dbc

social_housing=['七賢安居','美都安居','明仁好室','崇實安居','福山安居','清豐安居','鳳松安居','鳳誠安居','鳳翔安居','山明安居','水秀安居','仁武安居','大寮社會住宅','亞灣智慧公宅','岡山社會住宅','三民區新都段社會住宅','凱旋青樹共合宅','前金警察宿舍','鳳山共合宅']

def make_header(app) -> html.Header:
    """
    Returns a HTML Header element for the application Header.

    :param app: use get_asset_url function
    :return: HTML Header
    """
    return html.Header(
        className='width=100%',
        children=[
        # dbc.Row([
        #     dbc.Col(
            # children=[
            # Icon and title container
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            className="dash-title-container text-center",
                            children=[
                                html.Img(className="dash-icon", src=app.get_asset_url('logo.svg'),width=90),
                                html.H1(className="dash-title", children=[strings.APP_NAME]),
                            ],
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            html.Div(
                                children=[
                                    html.Label(
                                        className='text-muted',children=['社會住宅']
                                    ),
                                    dcc.Dropdown(
                                        id='social-housing-select-dpd',
                                        clearable=False,
                                        options=[{'label':sh,'value':sh} for sh in social_housing],
                                        value='明仁好室',
                                    )
                                ]
                            )   
                        ),width=4
                    )
                ]
            ),   
            # create navigator with buttons
            html.Nav(
                children=[
                    dcc.Tabs(
                        id="navigation-tabs",
                        value="tab-port-map",
                        children=[
                            dcc.Tab(
                                label=strings.TAB1_NAME,
                                value="tab-port-map",
                                className="dash-tab",
                                selected_className="dash-tab-selected",
                            ),
                            dcc.Tab(
                                label=strings.TAB2_NAME,
                                value="tab-port-stats",
                                className="dash-tab",
                                selected_className="dash-tab-selected",
                            ),
                            dcc.Tab(
                                label=strings.TAB3_NAME,
                                value="tab-port-compare",
                                className="dash-tab",
                                selected_className="dash-tab-selected",
                            ),
                        ],
                    ),
                    # TODO Dario - remove below button
                    # html.Button(id='btn-sidebar-request-port', className='btn-sidebar-request-port', children=[strings.BTN_REQUEST_PORT])
                ]
            )
        ]
    )
