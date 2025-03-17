import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

with open("house_embeddings.pkl", "rb") as f:
    house_embeddings = pickle.load(f)


nursing_houses = pd.read_excel("DataNursingHouses.ods", engine='odf')

def get_similar_nursing_homes(house_name, top_n=3):
    try:
        similarity_matrix = cosine_similarity(house_embeddings)

        query_index = nursing_houses[nursing_houses["Name"].replace("\u200b", "") == house_name.replace("\u200b", "")].index
        if query_index.empty:
            return f"ไม่พบบ้านพักชื่อ '{house_name}'"

        query_index = query_index[0]
        similarity_scores = similarity_matrix[query_index]

        similar_houses = sorted(
            [(i, similarity_scores[i]) for i in range(len(nursing_houses)) if i != query_index],
            key=lambda x: x[1], reverse=True
        )[:top_n]

        return [
            {
                "Name": nursing_houses.iloc[i]["Name"].replace("\u200b", ""),
                "price": nursing_houses.iloc[i]["price"],
                "similarity": round(score, 4)
            }
            for i, score in similar_houses
        ]
    except Exception as e:
        return []

# ทดลอง
# house_name = "สุขสบายเนอร์สซิงโฮม (It-carehome)"
# house_name = 'ข่วงผะหญา เนอร์สซิ่งโฮม ลำปาง'
# house_name = 'Homeoflove'
# recommendations = get_similar_nursing_homes(house_name, top_n=3)

# print(f"บ้านพักที่คล้ายกับ '{house_name}':\n")
# for rec in recommendations:
#     print(rec["Name"])

