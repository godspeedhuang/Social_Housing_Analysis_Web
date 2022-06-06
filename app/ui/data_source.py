from dash import html
import dash_bootstrap_components as dbc

def make_data_source()->html.Div:
    """
    Make Data seurce block in page's bottom.
    """
    return html.Div(
        className="wrapper",
        children=[
            dbc.Row(
                dbc.Col(
                    html.Div(id="main-area", className="main-area"),
                    width=12
                    # contact_modal.make_contact_modal(),
                )
            ),
            dbc.Row(
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.H4('資料來源',className="text-light text-center"),
                                        html.Div(
                                            children=[
                                                html.Ul(
                                                    children=[
                                                        html.Li(
                                                            children=['幼兒園：',
                                                            html.A(children=['高雄市政府教育局立案幼兒園名冊'],href='https://www.kh.edu.tw/forms/getDirectory/101')
                                                            ],
                                                        ),
                                                        html.Li(
                                                            children=['社會福利服務：',
                                                            html.A(children=['高雄市社會福利服務中心通訊錄'],href='https://topics.mohw.gov.tw/SS/cp-4528-48210-204.html')
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children=['身心障礙服務：',
                                                            html.A(children=['高雄市長期照顧中心-日間照顧長照機構一覽表'],href='https://ltc.kchb.gov.tw/service/info/1')
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children=['長期照顧服務：',
                                                            html.A(children=['高雄市長期照顧中心-日間照顧長照機構一覽表'],href='https://ltc.kchb.gov.tw/service/info/1')
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children=['社區活動：',
                                                            html.A(children=['高雄市政府資料開放平台-高雄市里活動中心'],href='https://data.kcg.gov.tw/dataset/actcenter')
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children=['托育服務：',
                                                            html.A(children=['高雄市政府社會局托嬰中心名冊'],href='https://socbu.kcg.gov.tw/index.php?prog=2&b_id=25&m_id=127&s_id=522')
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children=['租金資料：',
                                                            html.A(children=['內政部不動產交易實價查詢服務網'],href='https://lvr.land.moi.gov.tw/')
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children=['人口資料：',
                                                            html.A(children=['社會經濟資料服務平台'],href='https://segis.moi.gov.tw/STAT/Web/Platform/QueryInterface/STAT_QueryInterface.aspx?Type=1#')
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children=['周邊社區民眾參與表單：',
                                                            html.A(children=['表單'],href='https://forms.gle/quDbE2he85Bbpvfc7'),'、',
                                                            html.A(children=['表單回應資訊'],href='https://docs.google.com/spreadsheets/d/1Rbvuhpib2qHcHGFaBH8pHYVsezEI5JM0I9ZKAvm81Uw/edit?usp=sharing')
                                                            ]
                                                        ),
                                                        html.Li(
                                                            children=['社宅民眾參與表單：',
                                                            html.A(children=['表單'],href='https://forms.gle/xpAQTibyGmkJMWG5A'),'、',
                                                            html.A(children=['表單回應資訊'],href='https://docs.google.com/spreadsheets/d/1gFF_-EZ1gQgRyPf5dkVWnR8QWQEwUweSoF8-vjO6tbA/edit?usp=sharing')
                                                            ]
                                                        )],
                                                    className='text-light'
                                                )
                                            ],
                                            className=''
                                        )
                                    ],
                                    className='m-3'
                                ),
                            ],
                            className='border mt-3 rounded'
                        )
                        
                    ],
                )
            )
        ]
    )       