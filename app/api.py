import time

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
model = joblib.load("models/model.pkl")

instrumentator = Instrumentator().instrument(app)

class Transaction(BaseModel):
    """Transaction class: Schema validation for transaction data.
    """
    amount: float
    transaction_time: float
    user_age: int
    is_international: int

app.post("/predict")
def predict(transaction: Transaction):
    input_data = [[
        transaction.amount,
        transaction.transaction_time,
        transaction.user_age,
        transaction.is_international
    ]]
    
    prediction = model.predict(input_data)
    return {"fraud_prediction": int(prediction[0])}

instrumentator.expose(app)