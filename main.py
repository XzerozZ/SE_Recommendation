from fastapi import FastAPI
import uvicorn
from load_model import *

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "This is recommendation systems"}

@app.get("/cosine")
# nh_name ล่าสุดที่ user คลิ้กดู
def read_cosine(nh_name: str):
    recommendations = get_similar_nursing_homes(nh_name, top_n=3)

    recommendations = [
        {key: int(value) if isinstance(value, np.int64) else 
             float(value) if isinstance(value, np.float64) else value
         for key, value in r.items()}
        for r in recommendations
    ]

    return {"result": recommendations}

@app.get("/llm")
def read_llm():
    return {"message": "llm with RAG รอแปป"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8005, reload=True)
