import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from config.common import FIGURES, FEATURES, TARGET, SEED
from config.common import prepare, read_splits, save_json

train, valid, test = read_splits()
threshold = float(train[TARGET].median())
estimators = {
    "DummyMostFrequent": DummyClassifier(strategy="most_frequent"),
    "LogisticRegression": LogisticRegression(
        C=1.0, max_iter=2000, random_state=SEED
    )
}
rows = []
for name, estimator in estimators.items():
    model = Pipeline([("prepare", prepare()), ("model", estimator)])
    model.fit(train[FEATURES], (train[TARGET] >= threshold).astype(int))
    actual = (test[TARGET] >= threshold).astype(int)
    predicted = model.predict(test[FEATURES])
    rows.append({
        "model": name, "accuracy": accuracy_score(actual, predicted),
        "balanced_accuracy": balanced_accuracy_score(actual, predicted),
        "macro_f1": f1_score(actual, predicted, average="macro"),
        "confusion_matrix": confusion_matrix(actual, predicted).tolist()
    })
save_json("classification_metrics.json", {
    "threshold_train_median": threshold, "test_metrics": rows,
    "positive_class": "rentals >= training median; teaching rule only"
})
ConfusionMatrixDisplay.from_predictions(
    actual, predicted, display_labels=["Normale", "E lartë"],
    cmap="Blues", colorbar=False
)
plt.tight_layout()
plt.savefig(FIGURES / "05_confusion.png", dpi=150)
plt.close()
print("Pragu:", threshold, "Rezultatet:", rows)
