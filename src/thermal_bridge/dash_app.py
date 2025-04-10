import dash
import dash_bootstrap_components as dbc
import pandas as pd

from src.thermal_bridge.initialize import init_psi

psi = init_psi()
df = pd.DataFrame(psi.data)

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SPACELAB],
                meta_tags=[{'name'   : 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
