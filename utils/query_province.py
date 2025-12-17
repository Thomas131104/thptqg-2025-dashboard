import polars as pl
from data import FULL_SCORES

# Tỉnh cũ (giữ nguyên)
df_means_before = (
    FULL_SCORES.group_by(["Tổ hợp", "Tỉnh thành cũ"])
    .agg(pl.col("Tổng điểm tổ hợp").mean().alias("TB"))
    .collect()
)

# Tỉnh mới (giữ nguyên)
df_means_after = (
    FULL_SCORES.group_by(["Tổ hợp", "Tỉnh thành mới"])
    .agg(pl.col("Tổng điểm tổ hợp").mean().alias("TB"))
    .collect()
)
