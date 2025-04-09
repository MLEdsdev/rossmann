from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

# Define request body model
class PredictionRequest(BaseModel):
    Store: int
    DayOfWeek: int
    Year: int
    Month: int
    Day: int
    Customers: int
    Open: int
    Promo: int
    StateHoliday: int
    SchoolHoliday: int

class BulkPredictionRequest(BaseModel):
    data: list[PredictionRequest]

# Load pre-trained model (replace 'model.pkl' with your model file)=
def initialize_model(model_path: str):
    try:
        with open(model_path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Model file not found at {model_path}. Please ensure the file exists.")
        return None

# Initialize the model
model = initialize_model("model_training/xgb_model.pkl")

@app.post("/predict")
async def predict(request: BulkPredictionRequest):
    if model is None:
        return JSONResponse(content={"error": "Model not loaded"}, status_code=500)

    try:
        # Convert features to numpy array and make prediction
        # features = [[request.Store, request.DayOfWeek, request.Year, request.Month,     
        #              request.Day, request.Customers, request.Open, request.Promo,
        #              request.StateHoliday, request.SchoolHoliday]]
        # 
        features = np.array([[
            req.Store, req.DayOfWeek, req.Year, req.Month, req.Day,
            req.Customers, req.Open, req.Promo, req.StateHoliday, req.SchoolHoliday
        ] for req in request.data])
        prediction = model.predict(features)   
        # prediction = model.predict(request.data)
        return prediction.tolist()
    except Exception as e:
        return JSONResponse(content={"error": f"Prediction failed: {str(e)}"}, status_code=500)