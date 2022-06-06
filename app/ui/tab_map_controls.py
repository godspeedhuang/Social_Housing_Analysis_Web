from config import strings
from dash import dcc,html

def make_tab_port_map_controls(
    public_arr: list,
    public_val: str,
) -> html.Div:
    """
    Returns a HTML div of user controls found on top of the map tab.

    :param public_arr: list, all possible ports
    :param public_val: str, current port value
    :return: HTML div
    """
    return html.Div(
        className="tab-port-map-controls",
        children=[
            html.Div(
                className="tab-port-map-single-control-container area-a",
                children=[
                    html.Label(
                        className="control-label", children=[strings.LABEL_PUBLIC]
                    ),
                    dcc.Dropdown(
                        id="port-map-dropdown-port",
                        clearable=False,
                        options=[{"label": pub, "value": pub} for pub in public_arr],
                        value=public_val,
                    ),
                ],
            ),
            html.Div(className="tab-port-map-single-control-separator area-b"),
            # html.Div(
            #     className="tab-port-map-single-control-container area-c",
            #     children=[
            #         html.Label(
            #             className="control-label", children=[strings.LABEL_VESSEL]
            #         ),
            #         dcc.Dropdown(
            #             id="port-map-dropdown-vessel-type",
            #             clearable=False,
            #             options=[
            #                 {"label": vessel_type, "value": vessel_type}
            #                 for vessel_type in vessel_types_arr
            #             ],
            #             value=vessel_type_val,
            #         ),
            #     ],
            # ),
            # html.Div(className="tab-port-map-single-control-separator area-d"),
            # html.Div(
            #     className="tab-port-map-single-control-container date-grid area-e",
            #     children=[
            #         html.Div(
            #             className="tab-port-map-single-control-container-date",
            #             children=[
            #                 html.Label(
            #                     className="control-label", children=[strings.LABEL_YEAR]
            #                 ),
            #                 dcc.Dropdown(
            #                     id="port-map-dropdown-year",
            #                     clearable=False,
            #                     options=[
            #                         {"label": year, "value": year} for year in year_arr
            #                     ],
            #                     value=year_val,
            #                 ),
            #             ],
            #         ),
            #         html.Div(
            #             className="tab-port-map-single-control-separator smaller-line"
            #         ),
            #         html.Div(
            #             className="tab-port-map-single-control-container-date",
            #             children=[
            #                 html.Label(
            #                     className="control-label",
            #                     children=[strings.LABEL_MONTH],
            #                 ),
            #                 dcc.Dropdown(
            #                     id="port-map-dropdown-month",
            #                     clearable=False,
            #                     options=[
            #                         {"label": month, "value": month}
            #                         for month in month_arr
            #                     ],
            #                     value=month_val,
            #                 ),
            #             ],
            #         ),
            #     ],
            # ),
        ],
    )
