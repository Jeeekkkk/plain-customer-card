from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"messege":"Your Customer Card is now live."}
