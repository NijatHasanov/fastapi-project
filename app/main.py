from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Hotel Energy API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/metrics")
async def get_metrics():
    """
    Get real-time metrics from Raspberry Pi sensors
    """
    # Replace with actual sensor data from your Pi 400
    return {
        "energy_usage": 1250.5,  # kWh
        "occupancy": 78.3,       # percentage
        "savings": 320.8,        # dollars
        "integrations": 5        # number of active sensors
    }
