from dash import html,dcc
import dash_bootstrap_components as dbc
from app import left_panel_func,helpers
import geopandas as gpd
import pandas as pd
from app import helpers
import plotly.express as px

def make_left_panel(
    social_housing:gpd.GeoDataFrame,
    popu_filter:pd.DataFrame,
    rent:pd.DataFrame,
    higher_adhesion:list,
    public_geotable_name:dict,
    villcode_list:list,
    engine
)->html.Div:
    """
    Make Left Panel
    
    :param social_housing: gpd.GeoSeries, Social housing data by tab dropdown selection
    :param villcode_list: list
    :return: html.Div
    """
    higher_adhesion_data=helpers.get_public_strength(higher_adhesion,popu_filter,public_geotable_name,engine,villcode_list)

    return html.Div(children=[
            dbc.Row(
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                html.H4(children=[f"{social_housing['name'].values[0]} 基本資訊"],className='text-light'),
                            ],
                            className='m-3',
                        ),
                        html.Hr(),
                        html.Div(
                            children=[
                                html.Ul(
                                    children=[
                                        html.Li(children=[f"總戶數： {social_housing['總戶數'].values[0]:,.0f} 戶"]),
                                        html.Li(children=[f"房型(1房/2房/3房)： {social_housing['一房型'].values[0]:,.0f} 戶/ {social_housing['二房型'].values[0]:,.0f} 戶/ {social_housing['三房型'].values[0]:,.0f} 戶"]),
                                        html.Li(children=[f"基地面積： {social_housing['area'].values[0]:,.2f} 平方公尺"]),
                                        html.Li(children=[f"交通條件： {social_housing['交通條件'].values[0]}"]),
                                        html.Li(children=[f"其他區位條件： {social_housing['其他區位條件'].values[0]}"])
                                    ]
                                )
                            ]
                        )
                    
                    ],width=12,className='border border-secondary my-1 mx-3 rounded pb-3 text-light'
                )
            ),
            dbc.Row(
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                html.H3(children=['需求強度分析']),
                            ],className='m-3',
                        ),
                        html.Div([
                            dcc.Graph(figure=px.line_polar(higher_adhesion_data,r=higher_adhesion_data.iloc[0,:],theta=higher_adhesion,line_close=True))
                        ])
                    ],width=12,className='border border-secondary my-1 mx-3 rounded pb-3 text-light'
                )
            ),
            dbc.Row(
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                html.H4(children=['分析區域 基本資訊']),
                                html.Hr(),
                            ],
                            className='m-3'
                        ),
                        html.Div(
                            children=[
                                html.Div([
                                    html.H5(children=['人口結構'],className='text-center'),
                                    html.P(children=[
                                                left_panel_func.population_sum(popu_filter)
                                            ],className='text-center text-secondary'),
                                    html.P(children=["資料時間:110年06月"],className='text-center text-secondary'),
                                    dbc.Row([
                                        dbc.Col(
                                            children=[
                                                left_panel_func.population_3(popu_filter)
                                            ],width=12
                                        ),
                                        dbc.Col(
                                            children=[
                                                left_panel_func.population_5(popu_filter)
                                            ],width=12
                                        )]
                                    ),
                                ],className='mb-3'),
                                html.Div([
                                    html.H5(children=['區域租金'],className='text-center'),
                                    html.P(children=[
                                        f"有效樣本數： {rent['單價(元/坪)'].count()}筆"
                                    ],className='text-center text-secondary'),
                                    html.P(children=[
                                        f"平均租金： {rent['單價(元/坪)'].astype('float').mean():,.2f} 元/坪"
                                    ],className='text-center text-secondary'),
                                    html.P(children=["資料時間： 110年6月-111年6月"],className='text-center text-secondary'),
                                    html.Div(
                                        children=[
                                            left_panel_func.get_rent(rent)
                                        ]
                                    )    
                                ],className='mb-3'),
                            ]
                        ),
                    ],width=12,className='border border-secondary my-1 mx-3 rounded text-light pb-3'
                )
            ),
        ]
    )