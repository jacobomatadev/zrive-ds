# pylint: disable=invalid-name
import json
import pandas as pd
from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay
from sklearn.metrics import precision_recall_curve, auc

LABEL_COL = "outcome"
BOOLEAN_COLS = [
    "ordered_before",
    "abandoned_before",
    "active_snoozed",
    "set_as_regular",
]
CATEGORICAL_COLS = ["product_type", "vendor"]
DATE_COLS = [
    "created_at",
    "order_date",
]
IDS_COLS = ["order_id", "user_id", "variant_id"]
NUMERICAL_COLS = [
    "user_order_seq",
    "normalised_price",
    "discount_pct",
    "global_popularity",
    "count_adults",
    "count_children",
    "count_babies",
    "count_pets",
    "people_ex_baby",
    "days_since_purchase_variant_id",
    "avg_days_to_buy_variant_id",
    "std_days_to_buy_variant_id",
    "days_since_purchase_product_type",
    "avg_days_to_buy_product_type",
    "std_days_to_buy_product_type",
]


def load_data(file_path):
    df = pd.read_csv(file_path)
    return df[df.groupby("order_id")["outcome"].transform("sum") > 4]


def preprocess_data(df):
    y = df[LABEL_COL].astype(int)
    X = df.drop(columns=[LABEL_COL] + IDS_COLS)

    gss = GroupShuffleSplit(test_size=0.2, n_splits=1, random_state=19)
    train_idx, test_idx = next(gss.split(X, y, groups=df["user_id"]))

    X_train, X_test = X.iloc[train_idx].copy(), X.iloc[test_idx].copy()
    y_train, y_test = y.iloc[train_idx].copy(), y.iloc[test_idx].copy()

    with open("freq_maps.json", "r", encoding="utf-8") as f:
        freq_maps = json.load(f)

    for col in CATEGORICAL_COLS:
        X_train[col] = X_train[col].map(freq_maps[col]).fillna(0)
        X_test[col] = X_test[col].map(freq_maps[col]).fillna(0)

    for col in DATE_COLS:
        for df_ in (X_train, X_test):
            ts = pd.to_datetime(df_[col], errors="coerce")
            df_[col] = (ts - pd.Timestamp("1970-01-01")) // pd.Timedelta("1D")

    num_like = NUMERICAL_COLS + DATE_COLS + CATEGORICAL_COLS

    scaler = StandardScaler()
    X_train[num_like] = scaler.fit_transform(X_train[num_like])
    X_test[num_like] = scaler.transform(X_test[num_like])

    X_train[BOOLEAN_COLS] = X_train[BOOLEAN_COLS].fillna(False).astype(int)

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    param_grid = {
        "C": [0.1, 0.3, 1, 3, 10, 30, 100],
    }
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=19)
    grid_search = GridSearchCV(
        LogisticRegression(max_iter=3_000, random_state=19, class_weight="balanced"),
        param_grid,
        cv=skf,
        scoring="average_precision",
        n_jobs=-1,
        refit=True,
        verbose=2,
        return_train_score=True,
    )

    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    return best_model


def check_model(model, X_test, y_test):
    y_proba = model.predict_proba(X_test)[:, 1]
    print(f"AUC-ROC: {roc_auc_score(y_test, y_proba):.3f}")
    RocCurveDisplay.from_estimator(model, X_test, y_test)
    PrecisionRecallDisplay.from_estimator(model, X_test, y_test)

    def pr_auc(y_true, y_scores):
        precision, recall, _ = precision_recall_curve(y_true, y_scores)
        return auc(recall, precision)

    print(f"AUC-PR: {pr_auc(y_test, y_proba):.3f}")


def main():
    print("Loading and preprocessing data...")
    df = load_data(Path("../../data") / "feature_frame.csv")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    model = train_model(X_train, y_train)
    check_model(model, X_test, y_test)
    print("Model training and evaluation completed successfully.")


if __name__ == "__main__":
    main()
