import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import dash_bootstrap_components as dbc
from dash import dash_table, Input, Output, callback, html

from src.thermal_bridge.dash_app import psi

lt = datetime.now(ZoneInfo('Europe/Berlin'))
date_string = lt.strftime('%d.%m.%Y - %H:%M')

psi_search_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("gob.sv"),
            html.H6(id="productos_last_update"),
            html.Hr(),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H4("Presentaciones"),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='table-pres-adeq',
                data=[],
                columns=[{'name': n, 'id': i} for n, i in zip(
                    ['Waermebruecke', 'Zusatzinfo Waermebruecke', 'Bezeichnung', 'Psi-Wert', 'mit Referenzbauteil',
                     'ebz', 'W&P', 'VHAG', 'Datum', 'Nr.', 'BV', 'Name', 'Farbe'],
                    ['Waermebruecke', 'Zusatzinfo Waermebruecke', 'Bezeichnung', 'Psi-Wert', 'mit Referenzbauteil',
                     'ebz', 'W&P', 'VHAG', 'Datum', 'Nr.', 'BV', 'Name', 'Farbe'])],
                filter_action="native",
                sort_action="native",
                page_action='none',
                style_table={'height': '400px', 'overflowY': 'auto'},
                # style_cell={'textAlign': 'left'},
                style_cell={'textAlign': 'left',
                            'maxWidth' : '320px',
                            'minWidth' : '35px',
                            # 'textOverflow': 'ellipsis'
                            },
                style_data={
                    'whiteSpace': 'normal',
                    'height'    : 'auto',
                },
                # export_format="csv",
                fixed_rows={'headers': True},
            ),

            # html.Hr()
        ], width=12)
    ],
        className="mb-5"),
    html.Div(id='dummy-div-buscar'),

])


# this callback updates the tables when changing tabs
@callback(
    Output('table-pres-adeq', 'data'),
    Output('productos_last_update', 'children'),
    Input('dummy-div-buscar', 'children'))
def update_table(_):
    logging.debug("Callback buscar")
    data = list(psi.data)
    return (data,
            f"Status: {psi.last_update} | n° Einträge: {len(psi.data)}")
