from dash import html, Input, Output, dcc, callback
import dash
import dash_bootstrap_components as dbc



layout = html.Div(
    style={"display": "flex", "flexDirection": "column", "minHeight": "100vh"},
    children=[
        dcc.Location(id="url"),
        # Header
        html.Header(
            dbc.NavbarSimple(
                brand="Dashboard kỳ thi THPTQG năm 2025",
                color="primary",
                dark=True,
                children=[
                    dbc.NavItem(dbc.NavLink("Home", href="/", id="nav-home")),
                    dbc.NavItem(
                        dbc.NavLink("Main app", href="/main-app", id="nav-main")
                    ),
                    dbc.NavItem(dbc.NavLink("API", href="/api", id="api")),
                ],
            )
        ),
        # Nội dung (chiếm hết phần còn lại)
        dbc.Container(
            dash.page_container,
            fluid=True,
            className="bg-light mt-4",
            style={"flex": "1"},  # quan trọng để đẩy footer xuống
        ),
        # Footer (luôn nằm dưới cùng)
        html.Footer(
            dbc.Container("By Mus", className="text-center py-3 text-white"),
            className="bg-primary mt-4",
        ),
    ],
)


@callback(
    Output("nav-home", "disabled"),
    Output("nav-main", "disabled"),
    Output("api", "disabled"),
    Input("url", "pathname"),
)
def update_navbar(pathname):
    match pathname:
        case "/main-app":
            return False, True, False
        case "/":
            return True, False, False
        case "/api":
            return False, False, True
        case _:
            return False, False, False

