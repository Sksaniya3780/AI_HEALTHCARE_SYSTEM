import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# =====================================
# SAMPLE TRAINING DATA
# =====================================

np.random.seed(42)

rows = 1000

data = pd.DataFrame({
    "age": np.random.randint(18, 80, rows),
    "blood_pressure": np.random.randint(80, 180, rows),
    "sugar": np.random.randint(70, 250, rows),
    "cholesterol": np.random.randint(100, 350, rows),
    "bmi": np.random.uniform(18, 40, rows)
})

data["disease"] = (
    (
        (data["blood_pressure"] > 140) |
        (data["sugar"] > 180) |
        (data["cholesterol"] > 240)
    )
).astype(int)

X = data.drop("disease", axis=1)
y = data["disease"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

joblib.dump(
    model,
    "models/disease_model.pkl"
)

print("Disease model saved successfully")
train disease model