from fastapi import FastAPI
from routers import simulation
from routers import business

app = FastAPI(
    title="Battery Digital Twin API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Battery Digital Twin Backend Running 🚀"
    }
app.include_router(simulation.router)
app.include_router(business.router)