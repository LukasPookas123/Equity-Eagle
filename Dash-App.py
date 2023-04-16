import eikon as ek
import pandas as pd
from dash import Dash, Input, Output, dcc, html

# Eikon API key
ek.set_app_key('04c0e3f661bd49348d69c3aabedb8c0108cfd1e2')

# Retrieve stock data


def get_stock_data(symbol, start_date, end_date):
    df, err = ek.get_data(symbol, ['TR.ClosePrice.Date', 'TR.ClosePrice'],
                          {'SDate': start_date, 'EDate': end_date})
    return df


names = data[NAME_COLUMN_HERE].sort_values().unique()

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Fundamental Analysis"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Fundamental Analysis", className="header-title"
                ),
                html.P(
                    children=(
                        "Analyze extracted company data from Refinitiv"
                        " in the form of various charts"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Name", className="menu-title"),
                        dcc.Dropdown(
                            id="name-filter",
                            options=[
                                {"label": name, "value": name}
                                for name in names
                            ],
                            value="AAPL.O",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data[DATE_COLUMN_NAME].min(
                            ).date(),
                            max_date_allowed=data[DATE_COLUMN_NAME].max(
                            ).date(),
                            start_date=data[DATE_COLUMN_NAME].min().date(),
                            end_date=data[DATE_COLUMN_NAME].max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("name-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(name, start_date, end_date):
    """
    CHART BUILDER
    """

    # df = get_stock_data(symbol, start_date, end_date)

    # return charts


if __name__ == "__main__":
    app.run_server(debug=True)
