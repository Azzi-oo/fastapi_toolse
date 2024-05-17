from fastapi import FastAPI
# from fastapi.testclient import TestClient
app = FastAPI()


@app.get("/sum/")
def calculate_sum(a: int, b: int):
    return {"reselt": a + b}
