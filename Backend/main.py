import logging
from pathlib import Path
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger("SpamSense")

app = FastAPI()


#the React app to call this API

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


MODEL_PATH = Path(__file__).resolve().parent / "spam_pipeline.joblib"

try:
    pipeline = joblib.load(MODEL_PATH)
    print(f"Model loaded from {MODEL_PATH}")
except Exception:
    pipeline = None
    logger.exception("Could not load the model. Did you run read_data.py?")
    
class PredictRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, value):
        if value.strip() == "":
            raise ValueError("message must not be empty")
        return value.strip()


class PredictResponse(BaseModel):
    prediction: str          
    spam_probability: float  
    note: str                


#ERROR HANDLING
@app.exception_handler(RequestValidationError)
async def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": "message is required: 1 to 1000 characters, not blank."},
    )


@app.get("/")
def home():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model is not available.")

    try:
        label = pipeline.predict([request.message])[0]
        spam_index = list(pipeline.classes_).index("spam")
        spam_prob = float(pipeline.predict_proba([request.message])[0][spam_index])
    except Exception:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Prediction failed.")

    return PredictResponse(
        prediction=str(label),
        spam_probability=round(spam_prob, 2),
        note="Demo only.A 'ham' result does not mean the message is safe.",
    )