import pandas as pd
from config import strings
from dash import html
import geopandas as gpd
import dash_bootstrap_components as dbc

def make_tab_public_sip_cards(
    data:gpd.GeoDataFrame,
    public:str,
    popu_filter:pd.DataFrame,
) -> html.Div:
    """
    Returns HTML code for the cards in the Stats tab.

    :param data: gpd.GeoDataFrame, Public data
    :param public: str, public type
    :param popu_filter: str

    :return: HTML div
    """

    def make_single_sip_card(
        heading_1: str, info_1: int, heading_2: str, info_2:int, heading_3:str,info_3:int
    ) -> html.Div:
        """
        Returns HTML code for a single card in the tab1.

        :return: HTML div
        """
        return html.Div(
            className="sip-card-stats-single",
            children=[
                html.Div(
                    className="sip-card-title",
                    children=[
                        html.H3(children=[f"{heading_1} {info_1} "]),
                    ],
                ),
                html.Div(
                    className="sip-card-body",
                    children=[
                        html.P(children=[f"{heading_2} {info_2} "])
                    ],
                ),
                html.Div(
                    className="sip-card-footer",
                    children=[
                        html.P(children=[f"{heading_3} {info_3}"])
                    ],
                ),
            ],
        )

    # data_card_1 = 
    # data_card_2 = tab_stats.get_stats_card2_data(
    #     df=df_stop, port=port, vessel_type=vessel_type, year=year, month=month
    # )
    # data_card_3 = tab_stats.get_stats_card3_data(
    #     df=df, port=port, vessel_type=vessel_type, year=year, month=month
    # )
    analysis_list=['幼兒園','長期照顧服務','托育服務','身心障礙服務']
    if public in analysis_list:
        if public == '幼兒園':
            # card_1
            supply=data['核定招收人數'].astype('int64').sum()
            note_1='幼兒園核定招收人數總和'
            room=f"{data['核定招收人數'].count()} 間"
            #card_2
            demand=popu_filter['幼稚園人口數'].astype('int64').sum()
            note_2='3-6歲人口總數'
        elif public =='長期照顧服務':
            # card_1
            supply=data['核定收托人數'].astype('int64').sum()
            note_1='長照機構收托人數總和'
            room=f"{data['核定收托人數'].count()} 間"
            # card_2
            demand=popu_filter['65歲以上人口數'].astype('int64').sum()*0.039
            note_2='以65歲以上人口數 3.9% 推估'
        elif public =='托育服務':
            #card_1
            supply=data['核定招收人數'].astype('int64').sum()
            note_1='托嬰中心招收人數總和'
            room=f"{data['核定招收人數'].count()} 間"
            #card_2
            demand=popu_filter['托幼人口數'].astype('int64').sum()
            note_2='0-2歲人口總數'
        elif public =='身心障礙服務':
            #card_1
            supply=data['核定可收數'].astype('int64').sum()
            note_1="身心障礙機構收容人數總和"
            room=f"{data['核定可收數'].count()} 間"
            # card_2
            demand=popu_filter['總人數'].astype('int64').sum()*0.053
            note_2='以總人口數 5.3% 推估'
            
        
        ratio=supply/demand
        if ratio<0.2:
            strength=5
            note_3="供需比小於20%"
        elif ratio<0.4:
            strength=4
            note_3="供需比介於20%-40%"
        elif ratio<0.6:
            strength=3
            note_3="供需比介於40%-60%"
        elif ratio<0.8:
            strength=2
            note_3="強度2供需比介於60%-80%"
        else:
            strength=1
            note_3="供需比大於80%"
        
        inner=[
            dbc.Row(
                [dbc.Col([
                    html.Div(
                        make_single_sip_card(
                            heading_1='供給量：',
                            info_1=f"{supply:,} 人",
                            heading_2='備註：',
                            info_2=note_1,
                            heading_3='間數：',
                            info_3=room,
                        )
                    )
                ],class_name='rounded')]
            ),
            dbc.Row(
                [dbc.Col([
                    html.Div(
                        make_single_sip_card(
                            heading_1='潛在需求量：',
                            info_1=f"{demand:,.0f} 人",
                            heading_2='備註：',
                            info_2=note_2,
                            heading_3=' ',
                            info_3=' ',
                        )
                    )
                ],class_name='rounded')]
            ),
            dbc.Row(
                [dbc.Col([
                    html.Div(
                        make_single_sip_card(
                            heading_1='需求強度：',
                            info_1=strength,
                            heading_2='備註：',
                            info_2=note_3,
                            heading_3='供需比：',
                            info_3=f"{ratio*100:.2f}%",
                        )
                    )
                ],class_name='rounded')]
            )
        ]
        
    else:
        inner=[]

    # card_1=html.Div(
    #     make_single_sip_card(
    #         heading_1='供給量：',
    #         info_1=f"{supply:,} 人",
    #         heading_2='備註：',
    #         info_2=note_1,
    #         heading_3='間數：',
    #         info_3=room,
    #     )
    # )
    # card_2=html.Div(
    #     make_single_sip_card(
    #         heading_1='潛在需求量：',
    #         info_1=f"{demand:,.0f} 人",
    #         heading_2='備註：',
    #         info_2=note_2,
    #         heading_3='',
    #         info_3='',
    #     )
    # )
    # card_3=html.Div(
    #     make_single_sip_card(
    #         heading_1='需求強度：',
    #         info_1=strength,
    #         heading_2='備註：',
    #         info_2=note_3,
    #         heading_3='供需比：',
    #         info_3=f"{ratio*100:.2f}%",
    #     )
    # )

    return html.Div(
        className="stats-card-container",
        children=inner,
    )
