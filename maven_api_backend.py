
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from io import BytesIO
from insight_engine import run_all_insights

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InsightAction(BaseModel):
    type: str
    action: str
    supplier: str | None = None
    item: str | None = None
    savings: float | None = None
    note: str | None = None
    change: float | None = None

class InsightResponse(BaseModel):
    insights: list[InsightAction]

@app.post("/upload/", response_model=InsightResponse)
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents), sheet_name='Sheet1')

    dynamic_insights = run_all_insights(df)

    return InsightResponse(insights=dynamic_insights)
