from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash import callback_context as ctx
from data import FULL_COMBINATIONS, PRE_PROVINCES, POST_PROVINCES
from utils.query_data import cached_hist, cached_means


# ===============================================================
# 🎨 LAYOUT (FIX: Thêm click-info và state cho mode)
# ===============================================================
layout = dbc.Container(
    [
        html.H3(
            "Phân tích điểm thi theo tỉnh và tổ hợp môn",
            className="text-center mb-4 mt-3 fw-bold",
        ),
        dcc.Store(id="mode-store", data="before"),
        # --- Bộ điều khiển ---
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("Chọn loại bản đồ", className="fw-bold mb-2"),
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                "Trước cải cách",
                                id="btn-before",
                                color="primary",
                                active=True,
                                n_clicks=0,
                            ),
                            dbc.Button(
                                "Sau cải cách",
                                id="btn-after",
                                color="secondary",
                                active=False,
                                n_clicks=0,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.P("Chọn tổ hợp môn", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        id="combination-dropdown",
                        options=[
                            {"label": combo, "value": combo}
                            for combo in FULL_COMBINATIONS.select("Tổ hợp")
                            .collect()["Tổ hợp"]
                            .to_list()
                        ],
                        placeholder="Chọn tổ hợp môn",
                        multi=False,
                    ),
                ]
            ),
            className="mt-5 mb-4 shadow-sm",
        ),
        html.Small(
            "💡 Click vào tỉnh để xem phân bố điểm.",
            className="text-muted fst-italic mb-2",
        ),
        html.Div(id="click-info", className="alert alert-info text-center my-2"),
        # --- Hàng chính: bên trái là bản đồ, bên phải là histogram ---
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            dcc.Graph(
                                id="graph",
                                style={"flex": "1", "height": "100%", "width": "100%"},
                            ),
                            type="circle",
                            color="#0d6efd",
                        )
                    ],
                    width=6,
                    style={"display": "flex", "flexDirection": "column"},
                ),
                dbc.Col(
                    [
                        dcc.Loading(
                            dcc.Graph(id="hist-new", style={"flex": "1"}), type="circle"
                        ),
                        dcc.Loading(
                            dcc.Graph(id="hist-old", style={"flex": "1"}), type="circle"
                        ),
                    ],
                    width=6,
                    style={"display": "flex", "flexDirection": "column"},
                ),
            ]
        ),
    ],
    fluid=True,
    className="p-3",
)


# ===============================================================
# 3. CALLBACK 1: CẬP NHẬT BẢN ĐỒ
# ===============================================================
@callback(
    [Output("graph", "figure"), Output("mode-store", "data")],
    Input("combination-dropdown", "value"),
    Input("btn-before", "n_clicks"),
    Input("btn-after", "n_clicks"),
)
def update_map(combination, n_before, n_after):
    triggered = ctx.triggered_id
    is_after = (triggered == "btn-after") or (n_after > n_before)
    mode = "after" if is_after else "before"

    gdf = POST_PROVINCES if is_after else PRE_PROVINCES
    col_tinh = "Tỉnh thành mới" if is_after else "Tỉnh thành cũ"

    # Nếu chưa chọn tổ hợp → bản đồ rỗng TB=0
    if not combination:
        gdf_plot = gdf.copy()
        gdf_plot["TB"] = 0

    else:
        df_scores = cached_means(combination, mode).to_pandas()
        gdf_plot = gdf.merge(
            df_scores, left_on="ten_tinh", right_on=col_tinh, how="left"
        ).fillna({"TB": 0})

    fig = px.choropleth_mapbox(
        gdf_plot,
        geojson=gdf_plot.__geo_interface__,
        locations="ten_tinh",
        featureidkey="properties.ten_tinh",
        color="TB",
        color_continuous_scale="Viridis" if combination else "Greys",
        hover_name="ten_tinh",
        hover_data={"TB": ":.2f"},
        zoom=5,
        center={"lat": 16, "lon": 107},
        mapbox_style="carto-positron",
        opacity=0.8,
        title=f"TB điểm ({'Sau' if is_after else 'Trước'} cải cách) - {combination or '...' }",
    )

    fig.update_layout(height=900, width=550, margin=dict(r=0, t=50, l=0, b=0))

    return fig, mode


# ===============================================================
# 4. CALLBACK 2: CLICK TỈNH → 2 HISTOGRAM THEO CHƯƠNG TRÌNH MỚI/CŨ
# ===============================================================
@callback(
    [
        Output("hist-new", "figure"),
        Output("hist-old", "figure"),
        Output("click-info", "children"),
    ],
    Input("graph", "clickData"),
    State("combination-dropdown", "value"),
    State("mode-store", "data"),
    prevent_initial_call=True,
)
def update_histograms_by_program(clickData, combination, mode):
    # Nếu chưa click tỉnh hoặc chưa chọn tổ hợp
    if not combination:
        empty = go.Figure().add_annotation(
            text="Chưa chọn tổ hợp môn", x=0.5, y=0.5, showarrow=False
        )
        return empty, empty, "Chưa chọn"

    # Nếu chưa click tỉnh → mặc định vẽ histogram cả nước
    province = clickData["points"][0]["location"] if clickData else "Cả nước"

    # Nếu province = "Cả nước", lấy tất cả tỉnh
    provinces_to_use = None if province == "Cả nước" else province

    # Lấy dữ liệu
    if province == "Cả nước":
        # Lấy tất cả sĩ tử theo tổ hợp và chương trình
        scores_new = cached_hist(combination, "all", mode, True)
        scores_old = cached_hist(combination, "all", mode, False)
    else:
        scores_new = cached_hist(combination, province, mode, True)
        scores_old = cached_hist(combination, province, mode, False)

    # Vẽ histogram
    fig_new = px.histogram(
        x=scores_new,
        nbins=40,
        title=f"GDPT 2018 – {province}<br><sub>{len(scores_new):,} sĩ tử</sub>",
    ).update_layout(bargap=0.1, title_x=0.5)

    fig_old = px.histogram(
        x=scores_old,
        nbins=40,
        title=f"GDPT 2006 – {province}<br><sub>{len(scores_old):,} sĩ tử</sub>",
    ).update_layout(bargap=0.1, title_x=0.5)

    info_text = f"Tổng: {(len(scores_new) + len(scores_old)):,}<br>Mới: {len(scores_new):,} <br>Cũ: {len(scores_old):,}"
    info = dbc.Alert(
        [
            html.Strong(f"{province} ({'Sau' if mode=='after' else 'Trước'} cải cách)"),
            html.Br(),
            info_text,
        ],
        color="info",
        className="text-center",
    )

    return fig_new, fig_old, info
