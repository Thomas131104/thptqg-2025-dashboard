import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import polars as pl
import io

from data import (
    province_before_list,
    province_after_list,
    FULL_COMBINATIONS,
    FULL_SCORES,
)

dash.register_page(__name__, path="/api", name="Trang chủ")

# --- Danh sách tổ hợp môn ---
combo_list = FULL_COMBINATIONS.select("Tổ hợp").unique().collect()["Tổ hợp"].to_list()

# ==========================
# LAYOUT
# ==========================
layout = html.Div(
    [
        html.H2("Chọn dữ liệu tổ hợp và tổng điểm thi để tải"),
        html.Div(
            [
                # --- Loại bản đồ ---
                dbc.Row(
                    [
                        dbc.Col(html.P("Chọn loại bản đồ:"), width=3),
                        dbc.Col(
                            dcc.Dropdown(
                                id="province-type",
                                options=[
                                    {"label": "Trước sáp nhập", "value": "before"},
                                    {"label": "Sau sáp nhập", "value": "after"},
                                ],
                                value="before",
                                multi=False,
                            ),
                            width=9,
                        ),
                    ],
                    className="mt-3",
                ),
                # --- Phạm vi tỉnh ---
                dbc.Row(
                    [
                        dbc.Col(html.P("Phạm vi tỉnh:"), width=3),
                        dbc.Col(
                            dcc.RadioItems(
                                id="province-mode",
                                options=[
                                    {"label": "Tất cả tỉnh", "value": "all"},
                                    {"label": "Chọn tỉnh cụ thể", "value": "custom"},
                                ],
                                value="all",
                            ),
                            width=9,
                        ),
                    ],
                    className="mt-3",
                ),
                # --- Dropdown chọn tỉnh ---
                dbc.Row(
                    [
                        dbc.Col(html.P("Chọn tỉnh/thành:"), width=3),
                        dbc.Col(
                            dcc.Dropdown(
                                id="province-select",
                                multi=True,
                                placeholder="Chọn một hoặc nhiều tỉnh...",
                            ),
                            width=9,
                        ),
                    ],
                    className="mt-2",
                ),
                # --- Phạm vi tổ hợp ---
                dbc.Row(
                    [
                        dbc.Col(html.P("Phạm vi tổ hợp:"), width=3),
                        dbc.Col(
                            dcc.RadioItems(
                                id="combo-mode",
                                options=[
                                    {"label": "Tất cả tổ hợp", "value": "all"},
                                    {"label": "Chọn tổ hợp cụ thể", "value": "custom"},
                                ],
                                value="all",
                            ),
                            width=9,
                        ),
                    ],
                    className="mt-3",
                ),
                # --- Dropdown chọn tổ hợp ---
                dbc.Row(
                    [
                        dbc.Col(html.P("Chọn tổ hợp môn:"), width=3),
                        dbc.Col(
                            dcc.Dropdown(
                                id="combo-select",
                                options=[{"label": x, "value": x} for x in combo_list],
                                multi=True,
                                placeholder="Chọn một hoặc nhiều tổ hợp môn...",
                            ),
                            width=9,
                        ),
                    ],
                    className="mt-2",
                ),
                # --- Chọn định dạng file ---
                dbc.Row(
                    [
                        dbc.Col(html.P("Chọn định dạng file:"), width=3),
                        dbc.Col(
                            dcc.Dropdown(
                                id="file-format",
                                multi=False,
                                value="csv",
                                options=[
                                    {"label": "CSV", "value": "csv"},
                                    {"label": "TSV", "value": "tsv"},
                                    {"label": "Excel (XLSX)", "value": "xlsx"},
                                    {"label": "Parquet", "value": "parquet"},
                                ],
                            ),
                            width=9,
                        ),
                    ],
                    className="mt-3",
                ),
                # --- Nút tải dữ liệu ---
                dbc.Row(
                    [
                        dbc.Col(width=3),
                        dbc.Col(
                            [
                                html.Button(
                                    "Tải dữ liệu",
                                    id="download-button",
                                    className="btn btn-primary",
                                ),
                                dcc.Download(id="download-data"),
                            ],
                            width=9,
                        ),
                    ],
                    className="mt-4",
                ),
            ]
        ),
    ]
)


# ==========================
# Callback cập nhật danh sách tỉnh theo loại bản đồ
# ==========================
@callback(
    Output("province-select", "options"),
    Output("province-select", "value"),
    Input("province-type", "value"),
)
def update_province_list(province_type):
    if province_type == "after":
        options = [{"label": x, "value": x} for x in province_after_list]
    else:
        options = [{"label": x, "value": x} for x in province_before_list]
    return options, None


# ==========================
# Callback disable dropdown khi chọn ALL
# ==========================
@callback(Output("province-select", "disabled"), Input("province-mode", "value"))
def disable_province_dropdown(mode):
    return mode == "all"


@callback(Output("combo-select", "disabled"), Input("combo-mode", "value"))
def disable_combo_dropdown(mode):
    return mode == "all"


# ==========================
# Callback xuất dữ liệu
# ==========================
@callback(
    Output("download-data", "data"),
    Input("download-button", "n_clicks"),
    State("province-type", "value"),
    State("province-mode", "value"),
    State("province-select", "value"),
    State("combo-mode", "value"),
    State("combo-select", "value"),
    State("file-format", "value"),
    prevent_initial_call=True,
)
def export_data(
    n_clicks, province_type, province_mode, provinces, combo_mode, combos, file_format
):

    if not n_clicks:
        return dash.no_update

    # Chọn cột tỉnh
    province_col = "Tỉnh thành mới" if province_type == "after" else "Tỉnh thành cũ"
    df_lazy = FULL_SCORES

    # Lọc tỉnh nếu không chọn ALL
    if province_mode != "all" and provinces:
        df_lazy = df_lazy.filter(pl.col(province_col).is_in(provinces))

    # Lọc tổ hợp nếu không chọn ALL
    if combo_mode != "all" and combos:
        df_lazy = df_lazy.filter(pl.col("Tổ hợp").is_in(combos))

    df = df_lazy.collect()

    if df.is_empty():
        return dash.no_update

    # Xuất file
    if file_format == "csv":
        buffer = io.StringIO()
        df.write_csv(buffer)
        content = "\ufeff" + buffer.getvalue()
        return dict(content=content, filename="data.csv")

    if file_format == "tsv":
        buffer = io.StringIO()
        df.write_csv(buffer, separator="\t")
        content = "\ufeff" + buffer.getvalue()
        return dict(content=content, filename="data.tsv")

    if file_format == "xlsx":
        buffer = io.BytesIO()
        df.write_excel(buffer)
        return dict(
            content=buffer.getvalue(),
            filename="data.xlsx",
            type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    if file_format == "parquet":
        buffer = io.BytesIO()
        df.write_parquet(buffer)
        return dict(content=buffer.getvalue(), filename="data.parquet")

    return dash.no_update
