import json
import logging
from pathlib import Path

import dash_auth
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Output, Input

import src
from dash_app import app
from src import SRC_ROOT, DATA_DIR
from tabs.tab_psi_search import psi_search_layout

debug = False

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s, %(levelname)s, %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=DATA_DIR / "thermal.log",
)

if not debug:
    with open(SRC_ROOT.parent.parent / Path("credentials.json")) as f:
        credentials = json.load(f)
    username_password = credentials["thermal_bridge"]

    auth = dash_auth.BasicAuth(app, username_password)

app.title = "Wärmebrücken"

app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Wärmebrückendaten", tab_id="tab-psi", labelClassName="text-success font-weight-bold",
                        activeLabelClassName="text-danger"),
                dbc.Tab(label="Upload", tab_id="tab-upload", labelClassName="text-success font-weight-bold",
                        activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="tab-psi",
        ),
    ], className="mt-3"
)

title = html.H1("Wärmebrücken")
version = f"{src.__version__}"

app.layout = dbc.Container([
    dbc.Row([dbc.Col(title, md=10), dbc.Col(version, md=2)], align="center"),
    # html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
    html.Div(id='content', children=[]),
])


@app.callback(

    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-upload":
        # return upload_layout
        raise NotImplementedError
    elif tab_chosen == "tab-psi":
        return psi_search_layout

    return html.P("This shouldn't be displayed for now...")


if __name__ == '__main__':
    logging.debug(f"Starting index.py with debug set to {debug} ")
    # logging.info("This is an info message.")
    # logging.warning("This is a warning message.")
    # logging.error("This is an error message.")
    # logging.critical("This is a critical message.")
    app.title = "Wärmebrücken"
    app.run(debug=debug)
