from dash import html, dcc, Input, Output, callback, dash_table, State,no_update
from dash import callback_context as ctx
import dash_bootstrap_components as dbc
from data import (
    province_after_list,
    province_before_list,
    FULL_SCORES,
    FULL_COMBINATIONS,
)
import polars as pl
import plotly.express as px


# --- Layout ---
layout = html.Div(
    [
        # --- Nút chọn trước/sau cải cách ---
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
            id="reform-button",
        ),
        # --- Dropdown chọn tỉnh ---
        html.P("Chọn tỉnh thành trong danh sách", className="fw-bold mt-2"),
        dcc.Dropdown(
            id="province-dropdown",
            options=[{"label": "Cả nước", "value": "Cả nước"}]
            + [{"label": p, "value": p} for p in province_before_list],
            value="Cả nước",
            className="mb-3",
        ),
        # --- Dropdown chọn tổ hợp ---
        html.P("Chọn tổ hợp môn", className="fw-bold mt-2"),
        dcc.Dropdown(
            id="combination-dropdown",
            options=[
                {"label": combo, "value": combo}
                for combo in FULL_COMBINATIONS.select("Tổ hợp")
                .collect()["Tổ hợp"]
                .to_list()
            ],
            placeholder="Chọn tổ hợp môn",
            multi=True,
            className="mb-4",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    # --- Bảng kết quả ---
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "📊 Bảng thống kê điểm theo tổ hợp",
                                className="fw-bold text-center fs-5",
                            ),
                            dbc.CardBody([
                                dcc.Loading(
                                    id="table-loading",
                                    type="circle",
                                    color="#0d6efd",
                                    fullscreen=False,
                                    children=[
                                        dash_table.DataTable(
                                            id="summary-table",
                                            style_table={
                                                "overflowX": "auto",
                                                "border": "1px solid #dee2e6",
                                                "borderRadius": "0.5rem",
                                                "padding": "8px",
                                            },
                                            style_cell={
                                                "textAlign": "center",
                                                "padding": "8px",
                                                "fontSize": "15px",
                                            },
                                            style_header={
                                                "backgroundColor": "#f8f9fa",
                                                "fontWeight": "bold",
                                                "borderBottom": "2px solid #ccc",
                                            },
                                            page_size=20,
                                        )
                                    ],
                                ),
                                dbc.Button(
                                    "⬇️ Tải bảng thống kê",
                                    id="btn-download-summary",
                                    color="success",
                                    className="mt-2",
                                ),
                                dcc.Download(id="download-summary"),
                            ],
                                className="mt-3",
                            ),
                            
                        ],
                        className="mt-4 shadow-sm rounded-3",
                    ),
                    width=6,
                ),
                dbc.Col(html.Div(id="graph"), width=6),
            ]
        ),
    ],
    className="p-4",
)


# ======================
# HÀM LỌC DỮ LIỆU
# ======================
def filter_scores(full_scores, province, combinations, is_before, is_after):
    if not combinations:
        return pl.DataFrame()

    df = full_scores.filter(pl.col("Tổ hợp").is_in(combinations))

    if province != "Cả nước":
        if is_after:
            df = df.filter(pl.col("Tỉnh thành mới") == province)
        else:
            df = df.filter(pl.col("Tỉnh thành cũ") == province)

    return df.collect()


# ======================
# HÀM TẠO BẢNG
# ======================
def make_summary_table(df, combinations):
    if df.is_empty():
        cols = [
            {"name": "Thông tin", "id": "Thông tin"},
            {"name": "Giá trị", "id": "Giá trị"},
        ]
        data = [{"Thông tin": "Không có dữ liệu", "Giá trị": "-"}]
        return cols, data

    summary = []
    for combo in combinations:
        for prog_name, prog_flag in [("Cũ", False), ("Mới", True)]:
            sub = df.filter(
                (pl.col("Tổ hợp") == combo) & (pl.col("Chương trình mới") == prog_flag)
            )
            if sub.height == 0:
                continue

            stats = sub.select(
                [
                    pl.count().alias("Số lượng"),
                    pl.col("Tổng điểm tổ hợp").mean().round(2).alias("Điểm TB xét tốt nghiệp"),
                    pl.col("Tổng điểm tổ hợp").min().round(2).alias("Thấp nhất"),
                    pl.col("Tổng điểm tổ hợp").quantile(0.05, "nearest").round(2).alias("5% điểm thấp nhất"),
                    pl.col("Tổng điểm tổ hợp").quantile(0.25, "nearest").round(2).alias("25% điểm thấp nhất"),
                    pl.col("Tổng điểm tổ hợp").median().round(2).alias("Trung vị"),
                    pl.col("Tổng điểm tổ hợp").quantile(0.75, "nearest").round(2).alias("25% điểm cao nhất"),
                    pl.col("Tổng điểm tổ hợp").quantile(0.95, "nearest").round(2).alias("5% điểm cao nhất"),
                    pl.col("Tổng điểm tổ hợp").max().round(2).alias("Cao nhất"),
                    pl.col("Tổng điểm tổ hợp").std().round(2).alias("Độ lệch chuẩn"),
                    pl.col("Tổng điểm tổ hợp").skew().round(2).alias("Độ nhọn (skew)"),
                    pl.col("Tổng điểm tổ hợp").kurtosis().round(2).alias("Độ nhọn (kurtosis)"),
                ]
            ).to_dicts()[0]

            col_prefix = f"{combo}_{prog_name}"
            for k, v in stats.items():
                summary.append((k, col_prefix, v))

    df_summary = (
        pl.DataFrame(summary, schema=["Loại thống kê", "Cột", "Giá trị"], orient="row")
        .pivot(values="Giá trị", index=["Loại thống kê"], columns="Cột")
        .rename({"Loại thống kê": "Thông tin"})
    )

    columns = [{"name": c, "id": c} for c in df_summary.columns]
    data = df_summary.to_dicts()
    return columns, data


@callback(
    Output("download-summary", "data"),
    Input("btn-download-summary", "n_clicks"),
    State("summary-table", "data"),
    prevent_initial_call=True,
)
def download_summary(n_clicks, table_data):
    if not table_data:
        return no_update

    df = pl.DataFrame(table_data).to_pandas()

    return dcc.send_data_frame(
        df.to_excel,
        filename="thptqg_2025_summary.xlsx",
        index=False,
        engine="openpyxl"
    )


# ======================
# HÀM TẠO BIỂU ĐỒ
# ======================
def make_boxplot(df):
    if df.is_empty():
        return html.Div("Không có dữ liệu", className="text-center text-muted")

    pdf = df.select(["Tổ hợp", "Chương trình mới", "Tổng điểm tổ hợp"]).to_pandas()
    pdf["Chương trình"] = pdf["Chương trình mới"].map({True: "Mới", False: "Cũ"})

    fig = px.box(
        pdf,
        x="Tổ hợp",
        y="Tổng điểm tổ hợp",
        color="Tổ hợp",
        facet_row="Chương trình",
        points="outliers",
        title="📊 Phân phối điểm theo tổ hợp và chương trình học",
        labels={"Tổ hợp": "Tổ hợp môn", "Tổng điểm tổ hợp": "Tổng điểm"},
    )

    fig.update_layout(
        height=350 * pdf["Chương trình"].nunique(),
        showlegend=False,
        margin=dict(t=60, b=40, l=60, r=20),
        font=dict(size=13),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=18, family="Inter, sans-serif", color="#0d6efd"),
        yaxis=dict(range=[0, 30]),
    )

    fig.for_each_xaxis(lambda x: x.update(showgrid=False))
    fig.for_each_yaxis(
        lambda y: y.update(showgrid=True, gridcolor="rgba(220,220,220,0.3)")
    )

    return dcc.Graph(figure=fig, config={"displayModeBar": False})


# ======================
# CALLBACK: cập nhật dropdown tỉnh theo nút Before/After
# ======================
@callback(
    Output("province-dropdown", "options"),
    Output("province-dropdown", "value"),
    Input("btn-before", "n_clicks"),
    Input("btn-after", "n_clicks"),
)
def update_province_dropdown(n_before, n_after):
    triggered_id = ctx.triggered_id
    if triggered_id == "btn-after":
        options = [{"label": "Cả nước", "value": "Cả nước"}] + [
            {"label": p, "value": p} for p in province_after_list
        ]
    else:
        options = [{"label": "Cả nước", "value": "Cả nước"}] + [
            {"label": p, "value": p} for p in province_before_list
        ]
    return options, "Cả nước"


# ======================
# CALLBACK CHÍNH: tạo bảng + biểu đồ
# ======================
@callback(
    Output("summary-table", "columns"),
    Output("summary-table", "data"),
    Output("graph", "children"),
    Input("province-dropdown", "value"),
    Input("combination-dropdown", "value"),
    Input("btn-before", "n_clicks"),
    Input("btn-after", "n_clicks"),
    prevent_initial_call=True,
)
def update_summary_and_graph(province, combinations, n_before, n_after):
    triggered_id = ctx.triggered_id
    is_after = triggered_id == "btn-after"

    # Xử lý chưa chọn tổ hợp
    if not combinations:
        empty_cols = [{"name": "Thông tin", "id": "Thông tin"}, {"name": "Giá trị", "id": "Giá trị"}]
        empty_data = [{"Thông tin": "-", "Giá trị": "-"}]
        empty_graph = html.Div("Chưa chọn tỉnh hoặc tổ hợp môn", className="text-center text-muted")
        return empty_cols, empty_data, empty_graph

    # Lọc dữ liệu
    df = filter_scores(FULL_SCORES, province, combinations, not is_after, is_after)

    # Tạo bảng
    cols, data = make_summary_table(df, combinations)

    # Tạo biểu đồ
    graph = make_boxplot(df)

    return cols, data, graph