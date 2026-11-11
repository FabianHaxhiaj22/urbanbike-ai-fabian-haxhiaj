from pathlib import Path
import json
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
SEED = 42
TARGET = "rentals"
NUMERIC = [
    "rentals_lag1", "rentals_lag7", "rentals_mean7",
    "temp_c_lag7", "rain_mm_lag7", "wind_ms_lag7", "trend_days"
]
CATEGORIES = ["weekday", "month", "workingday", "holiday"]
FEATURES = NUMERIC + CATEGORIES
for folder in [DATA / "processed", DATA / "teaching", FIGURES]:
    folder.mkdir(parents=True, exist_ok=True)

def save_json(name, value):
    text = json.dumps(value, indent=2, ensure_ascii=False)
    (REPORTS / name).write_text(text, encoding="utf-8")

def read_splits():
    path = DATA / "processed" / "model_data.csv"
    data = pd.read_csv(path, parse_dates=["date"])
    train = data.loc[data.date <= "2012-04-30"].copy()
    valid = data.loc[data.date.between("2012-05-01", "2012-08-31")]
    test = data.loc[data.date > "2012-08-31"].copy()
    assert train.date.max() < valid.date.min()
    assert valid.date.max() < test.date.min()
    return train, valid, test

def prepare(scale=True):
    steps = [("fill", SimpleImputer(
        strategy="median", add_indicator=True
    ))]
    if scale:
        steps.append(("scale", StandardScaler()))
    categories = OneHotEncoder(
        handle_unknown="ignore", sparse_output=False
    )
    return ColumnTransformer([
        ("numbers", Pipeline(steps), NUMERIC),
        ("categories", categories, CATEGORIES)
    ])
