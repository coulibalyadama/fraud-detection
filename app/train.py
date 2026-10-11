import os

import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def generate_dataset(n=5000):

    np.random.seed(42)

    data = pd.DataFrame({
        "amount": np.random.randint(10, 1000, n),
        "transaction_time": np.random.uniform(0, 24, n),
        "user_age": np.random.randint(18, 70, n),
        "is_international": np.random.randint(0, 2, n),
    })

    data["fraud"] = (
        (data["amount"] > 800) & 
        (data["is_international"] == 1)
    ).astype(int)

    return data

def train():
    data = generate_dataset()

    X = data.drop("fraud", axis=1)
    y = data["fraud"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model.pkl")

    print("Model training completed successfully.")
    print(f"Model accuracy: {accuracy:.2f}")
    print("Model saved to 'models/model.pkl'.")

if __name__ == "__main__":
    train()