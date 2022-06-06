import folium
import numpy as np
import pandas as pd
from app import helpers
from config import strings
from dash import html,dash_table
import geopandas as gpd

def make_tab_port_map_map(
    social_housing: gpd.GeoDataFrame,
    data: gpd.GeoDataFrame,
    vill: gpd.GeoDataFrame,
    public: str,
    buffer_boundary:gpd.GeoDataFrame
) -> html.Div:
    """
    Makes the interactive map for the Map tab

    :param df: GeoPandas DataFrame, input data
    :param public: str, public type

    :return: HTML div with the embedded map    
    """

    def generate_popup(row: pd.Series) -> folium.Popup:
        """
        Makes a popup for a single map marker.

        :param row: Pandas Series, a single row of the dataset
        :return: Folium Popup object
        """
        if public == '幼兒園':
            inner = f"""
                    <b>{strings.KG_LABEL_NAME}：<b/>{row.幼兒園名稱}<br>
                    <b>{strings.KG_LABEL_ATTR}：<b/>{row.屬性}<br>
                    <b>{strings.KG_LABEL_NUM}：<b/>{row.核定招收人數}<br>
                """
        elif public == '社會福利服務':
            inner = f"""
                    <b>名稱：<b/>{row.機構單位名稱}<br>
                    <b>地址：<b/>{row.服務轄區}<br>
                    <b>地址：<b/>{row.電話}<br>
            """
        elif public == '身心障礙服務':
            inner = f"""
                    <b>名稱：<b/>{row.機構名稱}<br>
                    <b>服務對象：<b/>{row.屬性}<br>
                    <b>核定收容人數：<b/>{row.核定可收數}<br>
                    <b>實際收容人數：<b/>{row.目前已收數}<br>
                    <b>使用率：<b/>{row.使用率:.2f}<br>
            
            """
        elif public == '長期照顧服務':
            inner = f"""
                    <b>名稱：<b/>{row.名稱}<br>
                    <b>服務對象：<b/>{row.屬性}<br>
                    <b>核定收容人數：<b/>{row.核定收托人數}<br>
                    <b>實際收容人數：<b/>{row.使用規模}<br>
                    <b>使用率：<b/>{row.使用率:.2f}<br>

            """
        elif public == '文康休閒活動':
            inner = f"""
                <b>名稱：<b/>{row.名稱}<br>
            """
        elif public == '社區活動':
            inner = f"""
                    <b>名稱：<b/>{row.里活動中心名稱}<br>
                """
        elif public == '托育服務':
            inner = f"""
                    <b>名稱：<b/>{row.所名}<br>
                    <b>屬性：<b/>{row.屬性}<br>
                    <b>核定收容人數：<b/>{row.核定招收人數}<br>
                    <b>實際收容人數：<b/>{row.實際招收人數}<br>
                    <b>使用率：<b/>{row.使用率:.2f}<br>
                """

        html = f"""<div class='map-popup'>
                        {inner}
                    <div>"""

        iframe=folium.IFrame(html,width=300,height=90)
        return folium.Popup(iframe)

    def generate_social_housing_popup(row:gpd.GeoSeries) -> folium.Popup:
        """
        Make a popup for a social housing data.

        :param row: gpd.GeoSeries, social housing data
        :return: Folium Popup object
        """
        html = f"""
            <b>{strings.SOCIAL_HOUSING_LABEL_NAME}:<b/>{row['name'].values[0]} <br>
            <b>{strings.SOCIAL_HOUSING_LABEL_ORGAN}:<b>{row['organ'].values[0]} <br>
            <b>{strings.SOCIAL_HOUSING_HOUSEHOLD_SUN}:<b/>{row['總戶數'].values[0]:.0f}戶 <br>
        """
        iframe=folium.IFrame(html,width=300,height=90)
        return folium.Popup(iframe)

  
    # GET SOCIAL HOUSING COORDINATE   
    social_housing=social_housing.to_crs(epsg=4326)
    social_housing['centroid']=social_housing['geom'].centroid
    social_housing['center_lat']=social_housing.centroid.x
    social_housing['center_lng']=social_housing.centroid.y
    
    social_housing_centroid=[social_housing['center_lng'].values[0],social_housing['center_lat'].values[0]]
    # INIT FOLIUM MAP
    public_map = folium.Map(
        location=social_housing_centroid,
        zoom_start=12,
        tiles='CartoDB positron',
        control_scale=True # SCALE
    )

    # ADD VILL BOUNDARY
    folium.GeoJson(
        vill.to_json(),
        name='村里界'
    ).add_to(public_map)

    # ADD BUFFER BOUNDARY
    folium.GeoJson(
        buffer_boundary.to_json(),
        name='環域範圍'
    ).add_to(public_map)
    
    # ADD SOCIAL HOUSING BOUNDARY
    folium.GeoJson(
        social_housing['geom'].to_json(),
        name='社會住宅基地'
    ).add_to(public_map)


    my_icon= folium.CustomIcon(r'assets\img\icon_1.png',icon_size=(30,30),icon_anchor=(15.30))
    # ADD PUBLIC MARKER
    for row in data.itertuples(index=False):
        folium.Marker(
            location=[row.lat, row.lng], 
            popup=generate_popup(row),
            # color=helpers.generate_map_marker_color(public, row.屬性),
            # icon=my_icon                   
        ).add_to(public_map)
        # map_legend = helpers.generate_map_legend()
        # public_map.get_root().add_child(map_legend)

    # ADD SOCIAL HOUSING MARKER
    folium.Marker(
        location=social_housing_centroid,
        popup=generate_social_housing_popup(social_housing),
        icon=folium.Icon(icon='fa-house')
    ).add_to(public_map)

    folium.LayerControl().add_to(public_map)
    public_map.fit_bounds(public_map.get_bounds(),padding=(5,5))
    public_map.save("data/index.html")
    return html.Div(
        className="map-container",
        children=[html.Iframe(srcDoc=open("data/index.html", "r").read())],
    )


def make_tab_port_map_table(
    data: gpd.GeoDataFrame, 
    public: str
) -> html.Div:
    """
    Makes a table shown below the map on the Map tab.

    :param data: gpd.GeoDataFrame, input data
    :param public: str, public type
    """

    data = pd.DataFrame(data.drop(columns=['id','geom','VILLCODE','lat','lng']))

    return html.Div(
        className="map-table-container",
        children=[
            dash_table.DataTable(
                id="table",
                columns=[{"name": col, "id": col} for col in data.columns],
                data=data.to_dict("records"),
                page_size=15,
                sort_action="native",
                filter_action="native",
                style_cell={"padding": "15px 5px", "boxShadow": "0 0",},
                style_data={"border": "0px", "textAlign": "center"},
                style_header={
                    "padding": "2px 5px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                    "border": "none",
                    "backgroundColor": "transparent",
                },
                style_table={"overflowX": "auto", "width": "calc(100% - 26px)",},
                style_data_conditional=[
                    {
                        "if": {"state": "selected"},
                        "backgroundColor": "transparent",
                        "border": "0px solid transparent",
                    }
                ],
            )
        ],
    )
