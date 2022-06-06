from dash import dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import geopandas as gpd

def population_sum(
    popu_filter:pd.DataFrame
)->str:
    """
    return the sum population of select vill

    :param popu_filter: select population table by villcode
    :return: str, population sum
    """
    data=popu_filter[['總人數']].astype('int64')
    
    return f"區域人口總數： {data.sum().values[0]:,}人"
    


def population_3(
    popu_filter:pd.DataFrame
)->dcc.Graph:
    """
    Draw 3-step Population ratio Pie-chart
    
    :param popu_filter: select population table by villcode
    :return: dcc.Graph
    """
    data=popu_filter[['0-14歲人口數','15-64歲人口數','65歲以上人口數']].astype('int64')
    data=pd.DataFrame(data.sum(),columns=['人口數'])
    data['年齡區間']=data.index
    fig=px.pie(
        data,values=data['人口數'],
        names=data['年齡區間'],
        color_discrete_sequence=px.colors.sequential.RdBu,
        hole=.3,
        title='人口三階段年齡組圓餅圖')
    return dcc.Graph(
        figure=fig
    )
    

def population_5(
    popu_filter:pd.DataFrame
)->dcc.Graph:
    """
    Draw 5-ages Population Pyramid

    :param popu_filter: select population table by villcode
    :return: dcc.Graph
    """
    data=popu_filter[['0-4歲男性人口數','0-4歲女性人口數','5-9歲男性人口數','5-9歲女性人口數',
        '10-14歲男性人口數','10-14歲女性人口數','15-19歲男性人口數','15-19歲女性人口數',
        '20-24歲男性人口數','20-24歲女性人口數','25-29歲男性人口數','25-29歲女性人口數',
        '30-34歲男性人口數','30-34歲女性人口數','35-39歲男性人口數','35-39歲女性人口數',
        '40-44歲男性人口數','40-44歲女性人口數','45-49歲男性人口數','45-49歲女性人口數',
        '50-54歲男性人口數','50-54歲女性人口數','55-59歲男性人口數','55-59歲女性人口數',
        '60-64歲男性人口數','60-64歲女性人口數','65-69歲男性人口數','65-69歲女性人口數',
        '70-74歲男性人口數','70-74歲女性人口數','75-79歲男性人口數','75-79歲女性人口數',
        '80-84歲男性人口數','80-84歲女性人口數','85-89歲男性人口數','85-89歲女性人口數',
        '90-94歲男性人口數','90-94歲女性人口數','95-99歲男性人口數','95-99歲女性人口數',
        '100歲以上男性人口數','100歲以上女性人口數'
        ]].astype('int64')
    data=pd.DataFrame(data.sum(),columns=['人口數'])
    women_bin=data[[i%2==1 for i in range(len(data.index))]]
    women_bin=women_bin['人口數'].values
    women_bin=women_bin*-1
    men_bin=data[[i%2==0 for i in range(len(data.index))]]
    men_bin=men_bin['人口數'].values
    
    y=list(range(0,100,5))
    layout=go.Layout(yaxis=go.layout.YAxis(title='年齡'),
                    xaxis=go.layout.XAxis(title='人口數'),
                    barmode='overlay',
                    bargap=0.1
                    )
    data=[
        go.Bar(y=y,
                x=men_bin,
                orientation='h',
                name='男性',
                hoverinfo='x',
                marker=dict(color='powderblue')
        ),
        go.Bar(y=y,
            x=women_bin,
            orientation='h',
            name='女性',
            text=-1*women_bin.astype('int64'),
            hoverinfo='text',
            marker=dict(color='red')
        )]
    fig=go.Figure(data=data,layout=layout)
    return dcc.Graph(
        figure=fig
    )


def get_rent(
    rent:pd.DataFrame
)->dcc.Graph:
    """
    Draw a rent boxplot

    :param rent: pd.DataFrame, get social housing rent.
    :return: dcc.Graph, rent boxplot.
    """
    data=rent['單價(元/坪)'].astype('float')
    print(data.dtype)
    fig=go.Figure()
    fig.add_trace(
        go.Box(
            y=data,
            name='租金'
        )
    )
    return dcc.Graph(
        figure=fig
    )