import json
import sys
import numpy as np
import xgboost as xgb

_model = None


def _train_dummy_model() -> xgb.XGBClassifier:
    rng = np.random.default_rng(42)
    x = rng.uniform(0.0, 1.0, size=(220, 4))
    score = x[:, 0] * 35 + x[:, 1] * 400 + x[:, 2] * 8 + x[:, 3] * 3
    y = (score > 420).astype(np.int32)
    clf = xgb.XGBClassifier(
        n_estimators=24,
        max_depth=4,
        learning_rate=0.25,
        objective="binary:logistic",
        random_state=42,
        n_jobs=1,
    )
    clf.fit(x, y)
    return clf


def get_workout_model() -> xgb.XGBClassifier:
    global _model
    if _model is None:
        _model = _train_dummy_model()
    return _model


def predict_workout_quality(
    duration_minutes: float,
    calories_burned: float,
    intensity_score: float,
    sessions_last_week: float,
) -> tuple[str, float]:
    model = get_workout_model()
    row = np.array(
        [
            [
                min(duration_minutes / 120.0, 1.0),
                min(calories_burned / 1000.0, 1.0),
                min(intensity_score / 10.0, 1.0),
                min(sessions_last_week / 7.0, 1.0),
            ]
        ],
        dtype=np.float32,
    )
    proba_good = float(model.predict_proba(row)[0][1])
    label = "tốt" if proba_good >= 0.5 else "yếu"
    return label, proba_good


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    lab, pr = predict_workout_quality(45, 400, 6, 3)
    print(json.dumps({"label": lab, "probability": pr}, ensure_ascii=False))
