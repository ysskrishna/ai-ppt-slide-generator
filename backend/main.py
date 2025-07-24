from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import presentations
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to PPT Generator API"}

app.include_router(presentations.router, prefix="/api/v1/presentations", tags=["ppt"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)