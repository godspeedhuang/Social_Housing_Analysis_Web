from matplotlib.axis import XAxis
import numpy as np
import pandas as pd
import json
import os
from google.oauth2 import service_account
from apiclient import discovery
from dash import html, dash_table,dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


public_to_form_name={
        '幼兒園':'詢問貴戶針對 幼兒園 的需求程度比重',
        '社會福利服務':'詢問貴戶針對 社會福利服務 的需求程度比重',
        '身心障礙服務':'詢問貴戶針對 身心障礙服務 的需求程度比重',
        '長期照顧服務':'詢問貴戶針對 長期照顧服務 的需求程度比重',
        '文康休閒活動':'詢問貴戶針對 文康休閒活動 的需求程度比重',
        '社區活動':'詢問貴戶針對 社區活動 的需求程度比重',
        '托育服務':'詢問貴戶針對 托育服務 的需求程度比重',
        '青年創業空間':'詢問貴戶針對 青年創業空間 的需求程度比重',
        '圖書空間':'詢問貴戶針對 圖書空間 的需求程度比重',
        '會議空間':'詢問貴戶針對 會議空間 的需求程度比重',
}

def get_google_sheet(
    SPREADSHEET_ID,
    RANGE_NAME
)->list:
    """
    Get google sheet data.
    """
    file=open(r'data\abiding-cedar-352118-e0a2dead48a2.json',mode='r')
    service_account_info=json.load(file)
    creds=service_account.Credentials.from_service_account_info(service_account_info)

    service=discovery.build('sheets','v4',credentials=creds)

    sheet=service.spreadsheets()
    result=sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values=result.get('values',[])
    return values


def gsheet2df(values)->pd.DataFrame:
    """
    Convert google sheet data to pandas DataFrame.
    """
    header=values[0]
    rows=values[1:]
    data=pd.DataFrame(rows,columns=header)
    return data

def get_tidy_data(
    SPREADSHEET_ID:str,
    RANGE_NAME='表單回應 1!A1:M1000'
)->pd.DataFrame:
    gsheet=get_google_sheet(SPREADSHEET_ID,RANGE_NAME)
    data=gsheet2df(gsheet)
    # data=data.to_json(orient='split',force_ascii=False)
    return data


def get_data_mean(
    public_list:list,
    data:pd.DataFrame,
):
    data_mean=[data[public_to_form_name[col]].astype('int64').mean() for col in public_list]
    return  data_mean

def form_analysis_graph(
    public:str,
    data_1:pd.DataFrame,
    data_2:pd.DataFrame,
    higher_adhesion:list,
    lower_adhesion:list
)->html.Div:
    """
    :param data_1: surrounding people
    :param data_2: social housing people
    :return Html.Div:
    """
    
    def draw_line_polar(
        data:pd.DataFrame,
        column:list,
        title:str,
    )->px.line_polar:
        """
        draw line_polar for public=='全部'
        """
        data_mean=[data[public_to_form_name[col]].astype('int64').mean() for col in column]
        total=pd.DataFrame([data_mean],columns=column)
        return px.line_polar(total,r=data_mean,theta=column,line_close=True,title=title)

    def draw_bar(
        data:pd.DataFrame,
    ):
        """
        draw bar fig
        """
        fig=go.Figure(
            go.Bar(
                x=data.index,
                y=data
        ))
        fig.update_layout(
            xaxis_title='公共設施需求強度',
            yaxis_title='累積人數',
        )
        fig.update_xaxes(range=[0,6],dtick=1)
        return fig
    if public == '全部':
        # higher-adhesion-surrounding
        fig_1=draw_line_polar(data_1,higher_adhesion,'高附著設施需求強度雷達圖')
        # lower-adhesion-surrounding
        fig_2=draw_line_polar(data_1,lower_adhesion,'低附著設施需求強度雷達圖')
        # higher-adhesion-social-housing
        fig_3=draw_line_polar(data_2,higher_adhesion,'高附著設施需求強度雷達圖')
        # lower-adhesion-social-housing
        fig_4=draw_line_polar(data_2,lower_adhesion,'低附著設施需求強度雷達圖')
        
        inner=[
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=fig_1,className="m-3 p-0"),
                    dcc.Graph(figure=fig_2,className="m-3 p-0")
                ],width=6,class_name='border-end border-secondary'),
                dbc.Col([
                    dcc.Graph(figure=fig_3,className="m-3 p-0"),
                    dcc.Graph(figure=fig_4,className="m-3 p-0")
                ],width=6)
            ])
        ]
    else:
        data_select_1=pd.DataFrame(data_1[public_to_form_name[public]]).astype('int64')
        data_select_2=pd.DataFrame(data_2[public_to_form_name[public]]).astype('int64')
        data_select_1.columns=['strength']
        data_select_2.columns=['strength']
        data_select_1=data_select_1.value_counts('strength')
        data_select_2=data_select_2.value_counts('strength')
        # print(data_select_1.columns,data_select_2)
        fig_1 = draw_bar(data_select_1)
        fig_2 = draw_bar(data_select_2)
        

        inner=[
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=fig_1,className="m-3 p-0"),width=6,class_name='border-end border-secondary'
                ),
                dbc.Col(
                    dcc.Graph(figure=fig_2,className="m-3 p-0"),width=6
                )
            ])
        ]
    
    
    return html.Div(inner)
    

def make_form_table(
    data:pd.DataFrame,
) -> html.Div:
    """
    Make a table shown other people's opinions below the graph.
    """
    data=data['上述服務空間之外，您還希望社宅能提供那些項目服務?']
    # print(data)
    return html.Div(
        className='form-table-container',
        children=[
            dash_table.DataTable(
                id="table2",
                columns=['其他公共設施建議'],
                data=data.to_dict(),
                page_size=10,
                sort_action="native",
                filter_action="native",
                # style_cell={"padding": "15px 5px", "boxShadow": "0 0",},
                # style_data={"border": "0px", "textAlign": "center"},
                # style_header={
                #     "padding": "2px 5px",
                #     "fontWeight": "bold",
                #     "textAlign": "center",
                #     "border": "none",
                #     "backgroundColor": "transparent",
                # },
                # style_table={"overflowX": "auto", "width": "calc(100% - 26px)",},
                # style_data_conditional=[
                #     {
                #         "if": {"state": "selected"},
                #         "backgroundColor": "transparent",
                #         "border": "0px solid transparent",
                #     }
                # ],
            )
        ]
    )
