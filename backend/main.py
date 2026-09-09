from fastapi import FastAPI

from app.api.tribute import router as tribute_router

app = FastAPI(title="Sovenok Krish")

app.include_router(tribute_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "Sovenok Krish"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
