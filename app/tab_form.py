import matplotlib 
matplotlib.use('Agg') 
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

connect_to_google={"type": "service_account","project_id": "abiding-cedar-352118",  "private_key_id": "e0a2dead48a2c5ba76934b3cc84e78838affd8bb",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEugIBADANBgkqhkiG9w0BAQEFAASCBKQwggSgAgEAAoIBAQDBdVg/VDpznnO1\nek4Smtll8LZkMsY+HJ21dD1lOWfaTpgf7EpKKyessoK7CoAoe6+M+k6JHz2hovup\nJmNpzDT0Qf++dfBkU0Hx1lEeSpV891pFUx3jLL0KvJa/RyR2Ud2RD1MHtLN3liKm\nMcLLIGPSfGo6X1jrgl/Ngy4V9nf7Zva+zPHbYzYGkmvWJUErSB8BmQQvia9S3FeJ\nud+x5O4o4PbSyvesjbnBYeD9MppHoR0P6R46/hlUd0Ay4Z1GC1ZV+M65ybDMoqHZ\n4hmlj1c46CAMtSgBGPvGqqEZflvwW+dGlVwmaIQBrhF8SU9Kz6I26MRr1lDodf7l\nzXPk0zIVAgMBAAECgf9+g2X1AuPyQu1gHoEGcFx24Mi0qnHBDIiZ1KU/swIlWN6b\ncE56Q0Nv669rc/HPzDuoG/Kxbhetlcayiqc0Gm8HmQF4SWr1p+zaJWhbJodR7so1\n5rrMDEp8cNsEWpsoY3YhqNt5r022olglPMHUHQ2EPiF3ndv+NdodELTfACnbYfHk\nmvs0JO0LHI9gwX/Nq4EUDgVC3/54cFOqkIMBswGArNUUJ+RAm7xmasrpGwWyU9+t\nhFuRTHDwQ209cwZDBCF/NhhGFzw7ShokMJSr7Z99HsXICOBey+B46hw6yFykCztK\nTluwboJ5WGbYEqFdnyCdT7HQLbHqKA5q2YsylaUCgYEA+ppqd4ya62x6yg5tiPxG\nSUCl1Q8Mf/cSXxIUWlTL+Q77e3THLM+7m7WKdAD6H2i/vr0p0uziuhmpy2e5BHdY\nEN3Ux1chWLIrOPrAQYz2dgZt5MgL9yuTFVrYde/uFHsF8CL4xUdrRNUHVVwsnKbZ\nq4FZe6T2+PCtoQof07e5b58CgYEAxZ/jM12UurofI+kEexc33sUxOdUPqp+FL39d\n0or5hSQLLEMge1mpjPMiCJBrAJNEeYv9RAxUD9Qb5yBemQgtT4feqf5HQ4xD7aX5\nbOSSdoxUGLu5/cUrYOz61OjX+qnVeJzaRGOEjyJgxupzqu8uCci3qehhq7gA6eUJ\n02Rt8csCgYB6014lVAPGKXgROnsTLdphIs9kmqicu4MEl77j+zWxz1cQzk6ktvgT\nvCms66Gr7VI1cU9jcvk5D0T6Tc8P0lKWibM1NI5Cg6jNl5DNUAKoHESWYjoDHhdL\n2yfGvh7paNajOPDG+Fcp+GNMwg2XheuftJkgEd1+a7AeAvFQenbnrwKBgBcZNQkP\n6w5YKsObvLZWZGVZTwOfb5FVy89dZ63wKHHzYIrv3aANPtAGqvetSZRrohlCz3tg\npYKkHA7LrcLdPc6J5vCfk9zFTDs+pwSfQq8wf7PUXUzX+tX9XOP9wyC9MQJD8w8D\nQr8oGX+mb5aPFiZ2m2D0lFXpz9GGv7tBhcg5AoGAM4EG2Zm/ONfjJEIbqlw66rW2\n3MJ/R1nbEw5y246re1Rv9KMBeruaZuCC8YMhfHGw5KhJMDTKpJcNPeIWZy/LUA33\njie00LIEO0DNlOE4mWMFH/wlgDh+Wycsrdlv78yB+w/lHtDr6oRKqNxafynsF3zp\nyb1qWgx3lZ4EnBMSEoU=\n-----END PRIVATE KEY-----\n",
  "client_email": "dashboard@abiding-cedar-352118.iam.gserviceaccount.com",
  "client_id": "104136748761341213233",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dashboard%40abiding-cedar-352118.iam.gserviceaccount.com"
}

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
    # service_account_info=json.loads(connect_to_google)
    creds=service_account.Credentials.from_service_account_info(connect_to_google)

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
