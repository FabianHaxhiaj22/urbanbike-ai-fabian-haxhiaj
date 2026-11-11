import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.metrics import r2_score
from config.common import ROOT, REPORTS, FIGURES, SEED, FEATURES, TARGET
from config.common import prepare, read_splits, save_json

train, valid, test = read_splits()
estimators = {
    "DummyMean": DummyRegressor(strategy="mean"),
    "Ridge": Ridge(alpha=10.0),
    "RandomForest": RandomForestRegressor(
        n_estimators=200, max_depth=8, min_samples_leaf=4,
        random_state=SEED, n_jobs=1
    )
}
models = {}
for name, estimator in estimators.items():
    model = Pipeline([
        ("prepare", prepare(scale=name != "RandomForest")),
        ("model", estimator)
    ])
    model.fit(train[FEATURES], train[TARGET])
    models[name] = model

rows = []
predictions = {}
for split, frame in [("validation", valid), ("test", test)]:
    guesses = {"Yesterday": frame.rentals_lag1.to_numpy()}
    for name, model in models.items():
        guesses[name] = np.maximum(0, model.predict(frame[FEATURES]))
    for name, guess in guesses.items():
        rows.append({
            "split": split, "model": name, "n": len(frame),
            "MAE": mean_absolute_error(frame[TARGET], guess),
            "RMSE": np.sqrt(mean_squared_error(frame[TARGET], guess)),
            "R2": r2_score(frame[TARGET], guess)
        })
    predictions[split] = guesses
scores = pd.DataFrame(rows)
candidates = scores.loc[
    (scores.split == "validation") &
    scores.model.isin(["Ridge", "RandomForest"])
]
selected = candidates.sort_values("MAE").iloc[0]["model"]
scores.to_csv(REPORTS / "regression_metrics.csv", index=False)
output = test[["date", TARGET]].copy()
for name, guess in predictions["test"].items():
    output["prediction_" + name] = guess
output.to_csv(REPORTS / "test_predictions.csv", index=False)
(ROOT / "models").mkdir(exist_ok=True)
joblib.dump({"models": models, "selected": selected},
            ROOT / "models" / "regression.joblib")
splits = {}
for name, frame in [("train", train), ("validation", valid),
                    ("test", test)]:
    splits[name] = {"n": len(frame),
                    "start": str(frame.date.min().date()),
                    "end": str(frame.date.max().date())}
save_json("results_summary.json", {
    "features": FEATURES, "target": TARGET, "splits": splits,
    "selected_by_validation_MAE": selected, "metrics": rows,
    "training": "Train only; imputation learned inside each Pipeline.",
    "test_design": "One day ahead, past daily observations available."
})
plt.figure(figsize=(9, 4))
plt.plot(test.date, test.rentals, label="Reale")
plt.plot(test.date, predictions["test"][selected], label=selected)
plt.ylabel("Qira / ditë")
plt.title("Testi final, parashikime njëditore historike")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "04_predictions.png", dpi=150)
plt.close()
print(scores.round(3).to_string(index=False))
print("Modeli i zgjedhur nga validation:", selected)
