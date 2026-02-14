import argparse
import json
import os
from datetime import datetime

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


FEATURE_COLUMNS = [
    "zip_code",
    "beds",
    "baths",
    "sqft",
    "parking",
    "in_unit_laundry",
    "pet_friendly",
    "utilities_included",
]

TARGET_COLUMN = "rent"

"""
Builds a single Pipeline that includes preprocessing and the regression model 
(this guarantees the same transformations are used during training and later inference)
"""
def build_model() -> Pipeline:
    numeric_features = ["beds", "baths", "sqft"]
    categorical_features = ["zip_code"]
    boolean_features = ["parking", "in_unit_laundry", "pet_friendly", "utilities_included"]

    # Learn preprocessing params from training data
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("bool", "passthrough", boolean_features),
        ]
    )

    model = Ridge(alpha=1.0)

    return Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", model),
        ]
    )


def main(csv_path: str, outdir: str) -> None:
    df = pd.read_csv(csv_path)

    missing = [c for c in FEATURE_COLUMNS + [TARGET_COLUMN] if c not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the preprocessing
    pipeline = build_model()
    pipeline.fit(X_train, y_train)

    # Predict on test data
    preds = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, preds)

    os.makedirs(outdir, exist_ok=True)

    model_path = os.path.join(outdir, "model.joblib")
    joblib.dump(pipeline, model_path)

    metadata = {
        "mae": float(mae),
        "trained_at": datetime.utcnow().isoformat() + "Z",
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "model_type": "ridge_regression",
    }

    metadata_path = os.path.join(outdir, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved model to: {model_path}")
    print(f"Saved metadata to: {metadata_path}")
    print(f"MAE holdout test set: {mae:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to training CSV file")
    parser.add_argument("--outdir", required=True, help="Directory to write artifacts")
    args = parser.parse_args()

    main(csv_path=args.csv, outdir=args.outdir)
