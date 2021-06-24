
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# Imported but not used. This loads the callback functions into the web page.
import apps.model_builder.atmos_cond_callbacks

wind_rose_table = dash_table.DataTable(
    id = 'wind-rose-datatable',
    # data=dummy_df.to_dict("rows"),
    # columns=[{"name": i, "id": i} for i in dummy_df.columns],
    editable=True,
    style_table={'height': '600px', 'overflowY': 'auto'},
),

atmos_cond_inputs = dbc.Card(
    dbc.CardBody([
        html.H3("Wind farm atmospheric conditions.", className="card-text"),
        dbc.Row([
            dbc.Col(wind_rose_table),
            dbc.Col( dcc.Graph(id="wind-rose-graph") )
        ])
    ]),
    className="mt-3",
)

layout = html.Div([atmos_cond_inputs])