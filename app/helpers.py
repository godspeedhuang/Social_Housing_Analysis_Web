import pandas as pd
from branca.element import Template, MacroElement
from config import constants, strings, styles
import geopandas as gpd

def get_data(data_name:str,engine)->gpd.GeoDataFrame:
    """
    get data from postgres
    
    :param data_name: str, database table name
    :param engine: create engine object, postgres engine
    """
    sql=f'select * from public.{data_name}'
    data_file=gpd.GeoDataFrame.from_postgis(sql,engine,geom_col='geom')
    data_file.crs=4326
    return data_file

def get_nongeo_data(data_name:str,engine)->pd.DataFrame:
    """
    Get Non-Geo data from postgres

    :param data_name:str,database table name
    :param engine:create engine object, postgres engine
    """
    sql=f'select * from public.{data_name}'
    data_file=pd.read_sql(sql,engine)
    return data_file


def caculate_bufferr_village_code(
    social_housing:gpd.GeoSeries,
    village:gpd.GeoDataFrame,
    buffer_m:int=500
)->list:
    """
    get social housing buffer m meter's village code list

    :param social_housing: gpd.GeoSeries, target social housing data
    :param village: gpd.GeoDataFrame, Kaohsiung Village boundary geo data
    :param buffer_m: int, buffer meter default=500M
    """

    # generate buffer by social hosing centroid point
    social_housing_centroid=social_housing['geom'].centroid
    social_housing = social_housing_centroid.to_crs(epsg=3826)
    social_housing_buffer = social_housing.buffer(buffer_m)
    social_housing_buffer = social_housing_buffer.to_crs(epsg=4326)
    
    # convert buffer's data type to geodataframe
    buffer_dataframe=gpd.GeoDataFrame(social_housing_buffer,geometry=0)
    
    # add filter data
    buffer_dataframe['filter']='filter'
    
    # union buffer and village data
    union=gpd.overlay(village,buffer_dataframe,how='union')
    
    # filter union
    union = union[union['filter']=='filter']
    villcode_list=list(union['VILLCODE'])
    
    return villcode_list,buffer_dataframe


def calculate_public_strength(
	data:gpd.GeoDataFrame,
	public:str,
	popu_filter:pd.DataFrame
)->int:
	"""
	return public demand strength score 
	"""
	if public=='幼兒園':
		supply=data['核定招收人數'].astype('int64').sum()
		demand=popu_filter['幼稚園人口數'].astype('int64').sum()
	elif public =='長期照顧服務':
		supply=data['核定收托人數'].astype('int64').sum()
		demand=popu_filter['65歲以上人口數'].astype('int64').sum()*0.039
	elif public =='托育服務':
		supply=data['核定招收人數'].astype('int64').sum()
		demand=popu_filter['托幼人口數'].astype('int64').sum()
	elif public =='身心障礙服務':
		supply=data['核定可收數'].astype('int64').sum()
		demand=popu_filter['總人數'].astype('int64').sum()*0.053
	elif public =='社會福利服務':
		supply=0
		demand=1
	
	ratio=supply/demand
	
	if ratio<0.2:
		streng=5
	elif ratio<0.4:
		streng=4
	elif ratio<0.6:
		streng=3
	elif ratio<0.8:
		streng=2
	else:
		streng=1
	return streng



def get_public_strength(
	public_list:list,
	popu_filter:pd.DataFrame,
	public_geotable_name:dict,
	engine,
	villcode_list:list,
)->pd.DataFrame:
    # """
	# get public demand strength
	# """  
	strength=[]
	for pub in public_list:
		data=get_data(public_geotable_name[pub],engine)
		data = data[data['VILLCODE'].isin(villcode_list)]
		streng=calculate_public_strength(data=data,public=pub,popu_filter=popu_filter)
		strength.append(streng)
	strength_data=pd.DataFrame([strength],columns=public_list)
	return strength_data
	




def generate_map_legend() -> MacroElement:
    """
    Generates a legend for the map.

    :return: MacroElement, html added to the map
    """
    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Dashboard</title>
      <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
      
      <link rel="preconnect" href="https://fonts.gstatic.com">
      <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">

      <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
      <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>


    </head>
    <body>


    <div id='maplegend' class='maplegend' 
      style='
        position: absolute; 
        z-index:9999; 
        background-color:rgba(255, 255, 255, 0.8);
        border: 1px solid #D4D4D4;
        border-radius:6px; 
        padding: 10px; 
        font-size:14px; 
        right: 10px; 
        bottom: 23px;
      '>

    <div class='legend-scale'>
      <ul class='legend-labels'>
        <li><span style='background:#E87272;'></span>Unspecified</li>
        <li><span style='background:#7a0091;'></span>Navigation</li>
        <li><span style='background:#11498A;'></span>Fishing</li>
        <li><span style='background:#1A6D9B;'></span>Tug</li>
        <li><span style='background:#12A5B0;'></span>Passenger</li>
        <li><span style='background:#3A9971;'></span>Cargo</li>
        <li><span style='background:#79BD00;'></span>Tanker</li>
        <li><span style='background:#DBB657;'></span>Pleasure</li>
      </ul>
    </div>
    </div>

    </body>
    </html>

    <style type='text/css'>
      * {
        font-family: "Roboto", sans-serif;
      }

      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }

      .maplegend .legend-scale ul:last-child { 
        margin-bottom: 0px;
      }
      .maplegend .legend-scale ul li:last-child { 
        margin-bottom: 0px;
      }

    </style>
    {% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)
    return macro


def generate_map_marker_color(public: str, attr:str) -> str:
    """
    Returns a color hex code for a given ship category.

    :param category: str, ship category (vessel type)
    :return: str, hex code for the color
    """

    if public=='幼兒園':
      mappings = {
          strings.KG_MAPCOLOR_TYPE1:styles.COLOR_APPSILON_1,
          strings.KG_MAPCOLOR_TYPE2:styles.COLOR_APPSILON_2,
          strings.KG_MAPCOLOR_TYPE3:styles.COLOR_APPSILON_3,
          strings.KG_MAPCOLOR_TYPE4:styles.COLOR_APPSILON_4,
      }
    elif public == '社會福利服務':
        pass
    elif public == '身心障礙服務':
        mappings={}
    elif public == '長期照顧服務':
        mappings = {
            '失能、失智者':'red',
            '失智者':'red'
        }
    # elif public == '文康休閒服務':
    #     pass
    elif public == '社區活動':
        mappings = {
            '里活動中心':styles.COLOR_APPSILON_1
        }
    elif public == '托育服務':
        mappings = {
          '公共托嬰中心':styles.COLOR_APPSILON_1,
          '私立托嬰中心':styles.COLOR_APPSILON_2,
      }
    
    # mappings = {
    #     strings.STYPE_UNSPECIFIED: styles.COLOR_APPSILON_1,
    #     strings.STYPE_NAVIGATION: styles.COLOR_APPSILON_2,
    #     strings.STYPE_FISHING: styles.COLOR_APPSILON_3,
    #     strings.STYPE_TUG: styles.COLOR_APPSILON_4,
    #     strings.STYPE_PASSENGER: styles.COLOR_APPSILON_5,
    #     strings.STYPE_CARGO: styles.COLOR_APPSILON_6,
    #     strings.STYPE_TANKER: styles.COLOR_APPSILON_7,
    #     strings.STYPE_PLEASURE: styles.COLOR_APPSILON_8,
    # }
    return mappings[attr]
