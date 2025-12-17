import os
import geopandas as gpd
import polars as pl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FULL_SCORES = pl.scan_parquet(
    os.path.join(BASE_DIR, "score", "bang_diem_full.parquet")
).cache()
FULL_COMBINATIONS = pl.scan_csv(os.path.join(BASE_DIR, "score", "conversing-combinations.csv"))
FULL_GEOMS = pl.scan_csv(os.path.join(BASE_DIR, "geo", "conversing-provinces.csv"))
PRE_PROVINCES = gpd.read_file(
    os.path.join(BASE_DIR, "geo", "before-merging.geojson")
).to_crs(epsg=4326)
POST_PROVINCES = gpd.read_file(
    os.path.join(BASE_DIR, "geo", "after-merging.geojson")
).to_crs(epsg=4326)

province_before_list = (
    FULL_GEOMS.select("Tỉnh thành cũ")
    .unique()
    .sort(by="Tỉnh thành cũ")
    .collect()["Tỉnh thành cũ"]
    .to_list()
)

province_after_list = (
    FULL_GEOMS.select("Tỉnh thành mới")
    .unique()
    .sort(by="Tỉnh thành mới")
    .collect()["Tỉnh thành mới"]
    .to_list()
)
