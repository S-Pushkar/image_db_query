from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from sentence_transformers import SentenceTransformer
from pymilvus import connections, Collection
from dotenv import load_dotenv
import os

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

load_dotenv(".env.local")
ZILLIZ_ENDPOINT = os.getenv("ZILLIZ_ENDPOINT")
ZILLIZ_API_KEY = os.getenv("ZILLIZ_API_KEY")
connections.connect(uri=ZILLIZ_ENDPOINT, token=ZILLIZ_API_KEY)

COLLECTION_NAME = "ocr_text_vectors"
collection = Collection(COLLECTION_NAME)

class Item(BaseModel):
    email: EmailStr
    text: str

@app.post("/querytext/")
async def query_text(item: Item):
    vectors = model.encode(item.text)

    expr = f'email == "{item.email}"'
    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}

    results = collection.search(
        data=[vectors.tolist()],
        anns_field="embedding",
        param=search_params,
        limit=1,
        expr=expr,
        output_fields=["email", "timestamp", "image_path"]
    )

    result_data = []

    for hits in results:
        for hit in hits:
            hit_data = {
                "id": hit.id,
                "distance": hit.distance,
                "email": hit.entity.get("email"),
                "timestamp": hit.entity.get("timestamp"),
                "image_path": hit.entity.get("image_path")
            }
            result_data.append(hit_data)

    return {"results": result_data}