from fastapi import FastAPI
import uvicorn
from load_model import *

import faiss
import numpy as np
# from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import pandas as pd
from prompt import get_prompt


load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# embedding_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
embedding_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")
print(embedding_model.model_name)

vectorstore = FAISS.load_local("faiss_nursing_homes", embedding_model, allow_dangerous_deserialization=True)
llm = GoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=GOOGLE_API_KEY)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "This is recommendation systems"}

@app.get("/cosine")
# nh_name ล่าสุดที่ user คลิ้กดู
def read_cosine(nh_name: str):
    recommendations = get_similar_nursing_homes(nh_name, top_n=5)

    recommendations = [
        {key: int(value) if isinstance(value, np.int64) else 
             float(value) if isinstance(value, np.float64) else value
         for key, value in r.items()}
        for r in recommendations
    ]

    homes_name_list = [r["Name"] for r in recommendations]

    return {"result": homes_name_list}

@app.get("/llm")
def read_llm(nh_name: str):

    selected_house = nursing_houses[nursing_houses["Name"] == nh_name].iloc[0]
    selected_province, selected_price = selected_house["Province"],selected_house["price"]

    query_text = f"{selected_province}, {selected_price}"
    query_embedding = embedding_model.embed_query(query_text)

    similar_houses = vectorstore.similarity_search_by_vector(query_embedding, k=10)
    similar_houses_text = "\n".join([doc.page_content for doc in similar_houses])

    for i in similar_houses_text.split("\n"):
        print(i)

    system_prompt,user_prompt = get_prompt(similar_houses_text, nh_name, selected_province, selected_price)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt)
    ])

    response = llm.invoke(prompt.format())
    # print(response)
    return {"result": response.strip("[]\n").split(', ')}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8005, reload=True)
