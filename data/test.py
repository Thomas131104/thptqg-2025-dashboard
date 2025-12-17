import polars as pl
import geopandas as gpd
from data import (
    FULL_SCORES,
    FULL_COMBINATIONS,
    FULL_GEOMS,
    PRE_PROVINCES,
    POST_PROVINCES,
)

# Test FULL_SCORES
cols_scores = FULL_SCORES.collect_schema().names()
for c in ["Tỉnh thành mới", "Tỉnh thành cũ", "Tổng điểm tổ hợp", "Tổ hợp"]:
    assert c in cols_scores, f"{c} không có trong FULL_SCORES"

# Test GeoDataFrames
for c in ["ma_tinh", "geometry", "ten_tinh"]:
    assert c in POST_PROVINCES.columns, f"{c} không có trong POST_PROVINCES"
    assert c in PRE_PROVINCES.columns, f"{c} không có trong PRE_PROVINCES"


tinh_thanh_moi = (
    FULL_SCORES.select("Tỉnh thành mới").unique().collect()["Tỉnh thành mới"].to_list()
)
tinh_thanh_cu = (
    FULL_SCORES.select("Tỉnh thành cũ").unique().collect()["Tỉnh thành cũ"].to_list()
)


assert set(tinh_thanh_cu) == set(PRE_PROVINCES["ten_tinh"])
assert set(tinh_thanh_moi) == set(POST_PROVINCES["ten_tinh"])
