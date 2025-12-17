import os
import pickle
from functools import lru_cache
import polars as pl
import diskcache as dc
from data import FULL_SCORES

# ====================
# DiskCache Tier-2
# ====================
CACHE_DIR = "./cache"
os.makedirs(CACHE_DIR, exist_ok=True)
disk_cache = dc.Cache(CACHE_DIR)


# ====================
# Helper key
# ====================
def make_key(*args):
    """Tạo key duy nhất cho cache RAM / disk"""
    return pickle.dumps(args, protocol=pickle.HIGHEST_PROTOCOL)


# ====================
# cached_means: Tier-1 RAM + Tier-2 Disk
# ====================
@lru_cache(maxsize=512)  # Tier-1 RAM
def cached_means(combination: str, mode: str):
    """
    mode = "before" (Tỉnh thành cũ) hoặc "after" (Tỉnh thành mới)
    """
    key = make_key(combination, mode)

    # Kiểm tra DiskCache
    df_cached = disk_cache.get(key)
    if df_cached is not None:
        return df_cached

    # Compute từ FULL_SCORES
    col_tinh = "Tỉnh thành mới" if mode == "after" else "Tỉnh thành cũ"
    df = (
        FULL_SCORES.filter(pl.col("Tổ hợp") == combination)
        .group_by(col_tinh)
        .agg(pl.mean("Tổng điểm tổ hợp").round(2).alias("TB"))
        .collect()
    )

    # Lưu DiskCache
    disk_cache.set(key, df)
    return df


# ====================
# cached_hist: Tier-1 RAM + Tier-2 Disk
# ====================
@lru_cache(maxsize=2048)  # Tier-1 RAM
def cached_hist(combination: str, province: str, mode: str, program_new: bool):
    if province == "all":
        df = (
            FULL_SCORES.filter(
                (pl.col("Tổ hợp") == combination)
                & (pl.col("Chương trình mới") == program_new)
            )
            .select("Tổng điểm tổ hợp")
            .collect()
        )
        return df["Tổng điểm tổ hợp"].to_list()

    key = make_key(combination, province, mode, program_new)

    # Check DiskCache
    result = disk_cache.get(key)
    if result is not None:
        return result

    # Compute từ FULL_SCORES
    col_tinh = "Tỉnh thành mới" if mode == "after" else "Tỉnh thành cũ"
    df = (
        FULL_SCORES.filter(
            (pl.col("Tổ hợp") == combination)
            & (pl.col(col_tinh) == province)
            & (pl.col("Chương trình mới") == program_new)
        )
        .select("Tổng điểm tổ hợp")
        .collect()
    )

    result = df["Tổng điểm tổ hợp"].to_list()

    # Lưu DiskCache
    disk_cache.set(key, result)
    return result
