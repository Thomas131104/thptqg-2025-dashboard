import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from .inner_tab.by_province import layout as province_layout
from .inner_tab.by_combination import layout as combination_layout


dash.register_page(__name__, path="/main-app", name="Trang chủ")

layout = dbc.Container(
    [
        dbc.Row(
            [
                # Tab labels
                dbc.Col(
                    [
                        dbc.Tabs(
                            [
                                dbc.Tab(label="Theo tỉnh thành", tab_id="tab-1"),
                                dbc.Tab(label="Theo tổ hợp", tab_id="tab-2"),
                            ],
                            id="tabs",
                            active_tab="tab-1",
                        )
                    ],
                    width=12,
                )
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Nội dung tab
                dbc.Col(html.Div(id="tab-content"), width=12)
            ]
        ),
    ],
    fluid=True,
)


@callback(Output("tab-content", "children"), Input("tabs", "active_tab"))
def render_tab_content(active_tab):
    if active_tab == "tab-1":
        return province_layout
    elif active_tab == "tab-2":
        return combination_layout
    else:
        return html.Div([])
