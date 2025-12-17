import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/", name="Trang chủ", aliases=["/home"])


layout = html.Div(
    [
        html.H1("Trang chủ", className="text-center mt-4 mb-4"),
        # About me card
        dbc.Card(
            dbc.CardBody(
                [
                    html.Details(
                        [
                            html.Summary("About me", className="h3 mb-2"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Img(
                                            src="/assets/me.jpg",
                                            className="img-fluid rounded border border-primary",
                                            style={"maxWidth": "300px"}  # ảnh nhỏ gọn, không méo
                                        ),
                                        width="auto",
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            [
                                                html.P("Xin chào mọi người! Tôi là Mus, sinh viên năm 4 chuyên ngành Hệ thống thông tin."),
                                                html.P("Tôi đam mê phân tích dữ liệu, trực quan hóa thông tin và xây dựng các ứng dụng dựa trên Big Data."),
                                                html.P("Dự án này là cơ hội để tôi kết hợp kỹ năng lập trình, thống kê và trực quan hóa dữ liệu thực tế."),
                                            ]
                                        ),
                                        width=True,  # chiếm phần còn lại
                                    ),
                                ],
                                align="center",
                                className="g-3",
                            )
                        ]
                    )
                ]
            ),
            className="my-3 shadow-sm border p-3",
        ),
        # Project overview card
        dbc.Card(
            dbc.CardBody(
                [
                    html.Details(
                        [
                            html.Summary("Project Overview", className="h3 mb-2"),
                            html.P(
                                "Dự án này xây dựng một trang dashboard trực quan hóa dữ liệu kỳ thi THPT quốc gia năm 2025."
                                " Dashboard cung cấp thông tin chi tiết về phổ điểm theo từng tỉnh, theo tổ hợp môn và chương trình học,"
                                " trước và sau sáp nhập tỉnh thành."
                            ),
                            html.P("Các tính năng chính bao gồm:"),
                            html.Ul(
                                [
                                    html.Li(
                                        "Hiển thị bảng thống kê tổng hợp điểm thi theo tổ hợp môn và chương trình học."
                                    ),
                                    html.Li(
                                        "Trực quan hóa phân phối điểm bằng biểu đồ boxplot và histogram."
                                    ),
                                    html.Li(
                                        "Cho phép lọc dữ liệu theo tỉnh thành, tổ hợp môn và chương trình học."
                                    ),
                                    html.Li(
                                        "Tương tác với bản đồ để xem dữ liệu của từng tỉnh."
                                    ),
                                    html.Li(
                                        "Áp dụng caching để tăng tốc truy xuất dữ liệu lớn (Big Data)."
                                    ),
                                ]
                            ),
                            html.P(
                                "Dự án minh họa một ứng dụng thực tiễn của Big Data trong lĩnh vực giáo dục, "
                                "kết hợp phân tích dữ liệu lớn, trực quan hóa và thiết kế dashboard cho người dùng cuối."
                            ),
                        ]
                    )
                ]
            ),
            className="my-3 shadow-sm border p-3",
        ),
        # Motivation card
        dbc.Card(
            dbc.CardBody(
                [
                    html.Details(
                        [
                            html.Summary("Motivation", className="h3 mb-2"),
                            html.P(
                                "Mục tiêu của dự án là giúp người dùng, giáo viên và các cơ quan quản lý"
                                " có cái nhìn tổng quan và trực quan về kết quả thi THPT quốc gia."
                            ),
                            html.P(
                                "Việc phân tích và trực quan hóa dữ liệu này có thể hỗ trợ trong việc đánh giá chất lượng giáo dục,"
                                " so sánh phổ điểm giữa các tỉnh và chuẩn bị các báo cáo thống kê đáng tin cậy."
                            ),
                        ]
                    )
                ]
            ),
            className="my-3 shadow-sm border p-3",
        ),
    ]
)
