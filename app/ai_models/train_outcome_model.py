import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# =====================================
# GENERATE SAMPLE DATA
# =====================================

np.random.seed(42)

rows = 2000

data = pd.DataFrame({
    "age": np.random.randint(18, 90, rows),
    "severity": np.random.randint(1, 10, rows),
    "oxygen": np.random.randint(70, 100, rows),
    "heart_rate": np.random.randint(50, 160, rows),
    "hospital_days": np.random.randint(1, 30, rows)
})

# Outcome Target
data["recovery"] = (
    (
        (data["oxygen"] > 90) &
        (data["severity"] < 6)
    )
).astype(int)

X = data.drop("recovery", axis=1)
y = data["recovery"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)

model.fit(X_train, y_train)

joblib.dump(
    model,
    "models/outcome_model.pkl"
)

print("Outcome Model Saved Successfully")