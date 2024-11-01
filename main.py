from fastapi import FastAPI

app = FastAPI()

@app.get("/{number}")
async def root(number: int):
    return {"message": number}