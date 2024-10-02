# image_db_query

## Description

Exposes an API to query the vector database for the path of the image with the closest vector to the input query text.

## Usage
```uvicorn main:app --reload```

## Sample cURL request
```
curl -X POST "http://127.0.0.1:8000/querytext/" \
-H "Content-Type: application/json" \
-d '{"email": "abcd@gmail.com", "text": "your query"}'
```