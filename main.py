from dash import Dash,dcc,html
import pandas as pd
import dash_bootstrap_components as dbc
from app import helpers
from app.ui import (
    header,
    data_source,
    contact_modal,
    tab_map_controls,
    tab_public_sip_cards,
)
from app import tab_map,tab_form,tab_left_panel,tab_setting
from config import strings, constants
from dash.dependencies import Input, Output,State
import pyproj
from sqlalchemy import create_engine
import geopandas as gpd
import plotly.express as px
import numpy as np

# EXTERNAL SCRIPTS AND STYLES
external_scripts = ["https://kit.fontawesome.com/0bb0d79500.js"]

# SPREADSHEET_ID
SPREADSHEET_ID_1='1gFF_-EZ1gQgRyPf5dkVWnR8QWQEwUweSoF8-vjO6tbA'
SPREADSHEET_ID_2='1Rbvuhpib2qHcHGFaBH8pHYVsezEI5JM0I9ZKAvm81Uw'


# PUBLIC TYPE LIST
dpd_options_public=['幼兒園','托育服務','身心障礙服務','長期照顧服務','社會福利服務','社區活動','文康休閒活動']

# DATABASE TABLE NAME SETTING
public_geotable_name={
    '幼兒園':'高雄市幼兒園_村里',
    '社會福利服務':'高雄市社會福利機構_村里',
    '身心障礙服務':'高雄市身心障礙機構_村里',
    '長期照顧服務':'高雄市長照機構_失智失能_村里',
    '文康休閒活動':'高雄市文康休閒活動場所_村里',
    '社區活動':'高雄市里活動中心_村里',
    '托育服務':'高雄市公立私立托嬰中心_村里',
}

higher_adhesion=['幼兒園','社會福利服務','身心障礙服務','長期照顧服務','托育服務']
lower_adhesion=['文康休閒活動','社區活動','青年創業空間','圖書空間','會議空間']
form_public_list=higher_adhesion+lower_adhesion
# CONNECT TO DATABASE
pyproj.datadir.set_data_dir('C:\\Users\\godsp\\anaconda3\\envs\\geo_env\\Library\\share\\proj')
engine=create_engine('postgresql://postgres:5733@localhost:5432/testing')


# def dash_application(flask_app):
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}], # USE TO DISPLAY ON MOBILEPHOBE
    # url_base_pathname='/dash/',
    # server=flask_app,
    external_scripts=external_scripts,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server
app.title = strings.APP_NAME
app.config["suppress_callback_exceptions"] = True


# GET VILLAGE DATA
vill=helpers.get_data('高雄市村里界',engine=engine)    
# SET CURRENT PUBLIC TYPE
curr_public = strings.PUB_SELECTOR_INIT
curr_buffer=500


# GENERAL LAYOUT
app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                header.make_header(app),
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(
                data_source.make_data_source(),
                width=12
            )
        ),
        html.Footer(
            className="logo-footer",
            children=[
                html.Footer(
                    className="logo-footer-centering",
                    children=[
                        html.Div(
                            # href="https://appsilon.com/",
                            # target="_blank",
                            className="logo-footer-container",
                            children=[
                                html.H4(
                                    children=["Desinged by"], className="footer-element"
                                ),
                                html.Img(
                                    src=app.get_asset_url('banner.svg'),
                                    id="appsilon-icon",
                                    className="footer-element",
                                    width=100
                                ),
                                # html.H4(
                                #     children=[strings.TEAMNAME],
                                #     id="appsilon-text",
                                #     className="footer-element",
                                # ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ]
)


# TAB RENDERER
@app.callback(Output("main-area", "children"), [Input("navigation-tabs", "value")])
def render_tab(tab):
    """
    Renders content depending on the tab selected.

    :param tab: tab option selected
    :return: HTML div
    """
    if tab == "tab-port-map":
        return [
            html.Div(
                id="tab-port-map-container",
                className="tab-port-map-container",
                children=[
                    tab_map_controls.make_tab_port_map_controls(
                        public_arr=dpd_options_public,
                        public_val=curr_public,
                        buffer_val=curr_buffer,
                        attribute='map'
                    )
                ],
            )
        ]
    elif tab == "tab-port-stats":
        return [
            html.Div(
                id="tab-port-stats-container",
                className="tab-port-stats-container",
                children=[
                    tab_map_controls.make_tab_port_map_controls(
                        # public_arr=["全部公共設施"]+dpd_options_public,
                        public_arr=["全部"]+form_public_list,
                        # public_val='幼兒園'
                        public_val='全部',
                        buffer_val=curr_buffer,
                    ),
                    html.Div(
                        id='tab-form-container'
                    )
                    # html.Div(id='form-test-1',children=tab_form.get_tidy_data(),style={'display':'none'}),
                ],
            )
        ]
    elif tab == "tab-port-compare":
        return [
            html.Div(
                id="tab-port-compare-container",
                className="tab-port-compare-container",
                children=[
                    tab_setting.tab_higher_adhesion(
                        score_weighted=[0.25,0.25,0.5]
                    ),
                    tab_setting.tab_lower_adhesion(
                        score_weighted=[0.5,0.5]
                    )
                ],
            )
        ]


# MAP RENDERER (TAB 1)
@app.callback(
    Output("tab-port-map-container", "children"),
    [
        Input("port-map-dropdown-port", "value"),
        Input("social-housing-select-dpd",'value'),
        Input("buffer-boundary",'value')
        # Input("port-map-dropdown-vessel-type", "value"),
        # Input("port-map-dropdown-year", "value"),
        # Input("port-map-dropdown-month", "value"),
    ],
)
def update_port_map_tab(public,social_housing,buffer)->html.Div:
    """
    Renders content for the Map tab.

    :param port: str, port of interest
    :param vessel_type: str, vessel type of interest
    :param year: int, year of interest
    :param month: int, month of interest
    :return: HTML div
    """
    global curr_public,curr_buffer
    # global curr_vessel
    # global curr_year
    # global curr_month
    curr_public = public
    curr_buffer = buffer
    # curr_vessel = vessel_type
    # curr_year = year
    # curr_month = month
    
    # SOCIAL HOUSING SELECT
    social_housing_data=helpers.get_data('高雄市社會住宅範圍',engine=engine)
    social_housing_data=social_housing_data[social_housing_data['name']==social_housing] 

    # GET PUBLIC GEODATA FROM DATABASE BY PUBLIC NAME
    data = helpers.get_data(public_geotable_name[public],engine=engine)
    
    # GET AFTER BUFFER VILLCODE LIST
    global villcode_list, popu_filter
    villcode_list,buffer_boundary=helpers.caculate_bufferr_village_code(social_housing_data,vill,buffer_m=curr_buffer)

    # GET DATA BY FILTERING VILLCODE
    data = data[data['VILLCODE'].isin(villcode_list)]        
    # GET VILL BOUNDARY TO DISPLAY ON MAP BY FILTERING VILLCODE
    vill_filter = vill[vill['VILLCODE'].isin(villcode_list)]

    # GET POPULATION DATA
    population=helpers.get_nongeo_data('托幼_幼兒園_三階段_五齡組整合_2',engine=engine)
    popu_filter=population[population['VILLCODE'].isin(villcode_list)]

    # GET RENT DATA
    rent=helpers.get_nongeo_data('租金資料整理後',engine=engine)
    rent=rent[rent['name']==social_housing]

    return html.Div([
        # dbc.Row([
        #     dbc.Col(
        #         children=[
        #             tab_map_controls.make_tab_port_map_controls(
        #                 public_arr=dpd_options_public,
        #                 public_val=public,
        #             ),
        #         ],width=12
        #     ),
        # ]),
        dbc.Row([
            dbc.Col(
                children=[
                    tab_left_panel.make_left_panel(
                        social_housing=social_housing_data,
                        popu_filter=popu_filter,
                        rent=rent,
                        higher_adhesion=higher_adhesion,
                        public_geotable_name=public_geotable_name,
                        engine=engine,
                        villcode_list=villcode_list
                    )
                ],width=4
            ),
            dbc.Col(
                children=[
                    dbc.Col(
                        children=[
                            tab_map_controls.make_tab_port_map_controls(
                                public_arr=dpd_options_public,
                                public_val=public,
                                buffer_val=curr_buffer,
                                attribute='map'
                            ),
                            tab_public_sip_cards.make_tab_public_sip_cards(
                                data=data,
                                public=public,
                                popu_filter=popu_filter,
                            ),
                            tab_map.make_tab_port_map_map(
                                social_housing=social_housing_data,
                                data=data,
                                vill=vill_filter,
                                public=public,
                                buffer_boundary=buffer_boundary
                            ),
                            tab_map.make_tab_port_map_table(
                                data=data,
                                public=public
                            ),
                        ],width=12,class_name='my-1 p-1'
                    )
                ],width=8
            )
        ])
    ])

        
# STATS RENDERER (TAB 2)
@app.callback(    
    Output(component_id="tab-form-container", component_property='children'),
    [
        Input("port-map-dropdown-port", "value"),
        Input("social-housing-select-dpd",'value')
    ],
)
def update_port_stats_tab(public,social_housing)->html.Div:
    """
    Renders content for the Stats tab.

    :param port: str, port of interest
    :return: HTML div
    """
    
    # data_1:surrounding data_2:social housing
    data_1=tab_form.get_tidy_data(SPREADSHEET_ID=SPREADSHEET_ID_1)
    data_2=tab_form.get_tidy_data(SPREADSHEET_ID=SPREADSHEET_ID_2)
    
    data_1=data_1[data_1['請問您即將要入住的社會住宅為？']==social_housing]
    data_2=data_2[data_2['請問您即將要入住的社會住宅為？']==social_housing]
    
    ans_1=f"有效樣本數：{int(data_1.count().values[0])}"
    ans_2=f"有效樣本數：{int(data_2.count().values[0])}"
    
    
    # 再研究一下dash table怎麼用
    # form_table=tab_form.make_form_table(data)

    return  html.Div(
        className='form-container',
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[html.H3(children=["周邊社區民眾參與分析"],className="text-center text-light mt-3 fs-3")],width=6,class_name='border-end border-secondary'
                    ),
                    dbc.Col(
                        html.H3(children=["社宅民眾參與分析"],className="text-center text-light mt-3 fs-3"),width=6,
                    ),
                ]
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        html.P(children=[ans_1],id='form-num-1',className='text-center text-light'),width=6,class_name='border-end border-secondary'
                    ),
                    dbc.Col(
                        html.P(children=[ans_2],id='form-num-1',className='text-center text-light'),width=6,
                    )
                ]
            ),
            dbc.Row(
                children=[
                    tab_form.form_analysis_graph(public,data_1,data_2,higher_adhesion=higher_adhesion,lower_adhesion=lower_adhesion)
                ],
            ),
            # dbc.Row(
            #     children=[
            #         dbc.Col(children=[form_table]),
            #         dbc.Col(children=[form_table])
            #     ]
            # )
        ]
    )



# COMPARE RENDERER (TAB 3-高)
@app.callback(
    Output("tab-port-compare-container", "children"),
    [
        Input("social-housing-select-dpd",'value'),
        Input("submit-higher-button",'n_clicks'),
        State('surrounding-opendata-weighted','value'),
        State('surrounding-people-weighted','value'),
        State('social-housing-people-weighted','value'),
        Input("submit-lower-button",'n_clicks'),
        State('lower-surrounding-people-weighted','value'),
        State('lower-social-housing-people-weighted','value'),
    ],
)
def public_setting(social_housing,h_clicks,h_surr_open,h_surr_peo,h_soci_peo,
                                l_clicks,l_surr_peo,l_soci_peo):
    """
    Renders content for the public setting.

    :param port1: str, a port to compare
    :param port2:  str, a port to compare
    :param vessel_type: str, vessel type of interest
    :return: HTML div
    """
    
    data_1=tab_form.get_tidy_data(SPREADSHEET_ID=SPREADSHEET_ID_1)
    data_2=tab_form.get_tidy_data(SPREADSHEET_ID=SPREADSHEET_ID_2)
    data_1=data_1[data_1['請問您即將要入住的社會住宅為？']==social_housing]
    data_2=data_2[data_2['請問您即將要入住的社會住宅為？']==social_housing]
    # print(data_1)
    # print(data_2)
    
    
    h_data_surr=np.array(tab_form.get_data_mean(higher_adhesion,data_1))
    h_data_soci=np.array(tab_form.get_data_mean(higher_adhesion,data_2))
    
    h_surr_open_data=helpers.get_public_strength(
        public_list=higher_adhesion,
        popu_filter=popu_filter,
        public_geotable_name=public_geotable_name,
        engine=engine,
        villcode_list=villcode_list,
    )
    h_surr_open_data=np.array(h_surr_open_data.iloc[0].values)
    h_calculate=h_surr_open_data*float(h_surr_open)+h_data_surr*float(h_surr_peo)+h_data_soci*float(h_soci_peo)
    h_data=pd.DataFrame(h_calculate,index=higher_adhesion,columns=['公共設施需求強度'])
    h_data=h_data.sort_values(by=['公共設施需求強度'])
    fig_1=px.bar(h_data,orientation='h')

    l_data_surr=np.array(tab_form.get_data_mean(lower_adhesion,data_1))
    l_data_soci=np.array(tab_form.get_data_mean(lower_adhesion,data_2))
    l_calculate=l_data_surr*float(l_surr_peo)+l_data_soci*float(l_soci_peo)
    l_data=pd.DataFrame(l_calculate,index=lower_adhesion,columns=['公共設施需求強度'])
    l_data=l_data.sort_values(by=['公共設施需求強度'])
    fig_2=px.bar(l_data,orientation='h')        
            

    return html.Div(
        children=[
            html.Div(
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                html.H3(children=['高附著力公共設施需求計算'],className='text-center'),
                                tab_setting.tab_higher_adhesion([h_surr_open,h_surr_peo,h_soci_peo])
                            ],className='p-3')
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Img(src=app.get_asset_url('higher_.png'),width='100%'),
                            ],width=6,className='p-2'),
                            dbc.Col([
                                dcc.Graph(figure=fig_1),
                            ],width=6,className='p-2')
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.H3(children=['低附著力公共設施需求計算'],className='text-center'),
                                tab_setting.tab_lower_adhesion([l_surr_peo,l_soci_peo])
                            ],className='p-3')
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Img(src=app.get_asset_url('lower_.png'),width='100%'),
                            ],width=6,className='p-2'),
                            dbc.Col([
                                dcc.Graph(figure=fig_2),
                            ],width=6,className='p-2')
                        ])
                        # dbc.Row([
                        #     dbc.Col([

                        #     ],width=4),
                        #     dbc.Col(['test'],width=8)
                        # ])
                    ],className='text-light')
                ],className='border border-secondary rounded m-2 mt-2'),
            ),
            
            dbc.Row([]),
        ]
    )


# COMPARE RENDERER (TAB 3-低)
# @app.callback(
#     Output("tab-port-compare-container", "children"),
#     [
#         Input("social-housing-select-dpd",'value'),
        
#     ],
# )
# def public_setting(social_housing,l_clicks,l_surr_peo,l_soci_peo):
    # """
    # Renders content for the public setting.

    # :param port1: str, a port to compare
    # :param port2:  str, a port to compare
    # :param vessel_type: str, vessel type of interest
    # :return: HTML div
    # """

    # data_1=tab_form.get_tidy_data(SPREADSHEET_ID=SPREADSHEET_ID_1)
    # data_2=tab_form.get_tidy_data(SPREADSHEET_ID=SPREADSHEET_ID_2)
    # data_1=data_1[data_1['請問您即將要入住的社會住宅為？']==social_housing]
    # data_2=data_2[data_2['請問您即將要入住的社會住宅為？']==social_housing]
    # # print(data_1)
    # # print(data_2)
    # h_data_surr=np.array(tab_form.get_data_mean(higher_adhesion,data_1))
    # h_data_soci=np.array(tab_form.get_data_mean(higher_adhesion,data_2))
    
    # h_surr_open_data=helpers.get_public_strength(
    #     public_list=higher_adhesion,
    #     popu_filter=popu_filter,
    #     public_geotable_name=public_geotable_name,
    #     engine=engine,
    #     villcode_list=villcode_list,
    # )
    # h_surr_open_data=np.array(h_surr_open_data.iloc[0].values)
    # h_calculate=h_surr_open_data*float(h_surr_open)+h_data_surr*float(h_surr_peo)+h_data_soci*float(h_soci_peo)
    # h_data=pd.DataFrame(h_calculate,index=higher_adhesion,columns=['公共設施需求強度'])
    # h_data=h_data.sort_values(by=['公共設施需求強度'])
    # fig=px.bar(h_data,orientation='h')
    # print(h_surr_open,h_surr_peo,h_soci_peo)

    # return html.Div(
    #     children=[
    #         html.Div(
    #             dbc.Row([
    #                 dbc.Col([
    #                     dbc.Row([
    #                         dbc.Col([
    #                             html.H3(children=['高附著力公共設施需求計算'],className='text-center'),
    #                             tab_setting.tab_higher_adhesion([h_surr_open,h_surr_peo,h_soci_peo])
    #                         ],className='p-3')
    #                     ]),
    #                     dbc.Row([
    #                         dbc.Col([
    #                             html.Img(src=app.get_asset_url('higher_.png'),width='100%'),
    #                         ],width=6,className='p-2'),
    #                         dbc.Col([
    #                             dcc.Graph(figure=fig),
    #                         ],width=6,className='p-2')
    #                     ])
                        # dbc.Row([
                        #     dbc.Col([

                        #     ],width=4),
                        #     dbc.Col(['test'],width=8)
                        # ])
    #                 ],className='text-light')
    #             ],className='border border-secondary rounded m-2 mt-2'),
    #         ),
            
    #         dbc.Row([]),
    #     ]
    # )



# # COMPARE TAB DROPDOWNS
# @app.callback(
#     Output("port-compare-port-1-dpd", "options"),
#     [Input("port-compare-port-2-dpd", "value")],
# )
# def update_options_dpd1(dpd2_val) -> list:
#     """
#     Updates the contents of the first dropdown menu based of the value of the second dropdown.

#     :param dpd2_val: str, second dropdown value
#     :return: list of dictionaries, labels and values
#     """
#     all_options = [
#         strings.CITY_GDANSK,
#         strings.CITY_GDYNIA,
#         strings.CITY_KALINGRAD,
#         strings.CITY_KLAIPEDA,
#         strings.CITY_STPETERBURG,
#     ]
#     all_options.remove(dpd2_val)
#     options = [{"label": opt, "value": opt} for opt in all_options]
#     return options


# @app.callback(
#     Output("port-compare-port-2-dpd", "options"),
#     [Input("port-compare-port-1-dpd", "value")],
# )
# def update_options_dpd2(dpd1_val):
#     """
#     Updates the contents of the second dropdown menu based of the value of the first dropdown.

#     :param dpd1_val: str, first dropdown value
#     :return: list of dictionaries, labels and values
#     """
#     all_options = [
#         strings.CITY_GDANSK,
#         strings.CITY_GDYNIA,
#         strings.CITY_KALINGRAD,
#         strings.CITY_KLAIPEDA,
#         strings.CITY_STPETERBURG,
#     ]
#     all_options.remove(dpd1_val)
#     options = [{"label": opt, "value": opt} for opt in all_options]
#     return options

# return app

if __name__ == "__main__":
    # app.run_server(host='0.0.0.0', port=9000) # production
    app.run_server(debug=True)  # development
    # app.run_server()
