from fastapi import FastAPI
from api.routes import cheque_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Cheque Fraud Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for now allow all, later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register cheque routes
app.include_router(cheque_routes.router, prefix="/api/cheque", tags=["Cheque"])

@app.get("/")
def root():
    return {"message": "Cheque Fraud Detection API is running"}
cd frontend