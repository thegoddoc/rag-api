from fastapi import APIRouter, File, UploadFile, HTTPException
from scripts.pydant import IngestRequest
from scripts.build_index import VectoreStore
from configs.config import rag_config
import os
from pathlib import Path

router = APIRouter(prefix="/ingest", tags=["ingest"])

@app.post('/ingest')
async def ingest(req:IngestRequest, background_tasks:BackgroundTasks):
    # background_tasks.add_task(index_document, req.title, req.text, req.metadata)
    background_tasks.add_task(build_index, req.batch_size)
    return {"status":"accepted", "BATCH SIZE: ": req.batch_size}
    # VectoreStore

def build_index(batch_size:int, embedder):
    vs = VectoreStore(embedder=embedder,
                      vector_path=rag_config['EMBEDDING_FOLDER'],
                      client=client,collection=collection , 
                      collection_name=collection_name
                      )
    i = '.'
    while not embedder:
        for i in range(4):
            print(f'\r LOADING: {"."*i}',end=' ')
        print(f'EMBEDDER NOT READY yet')
    vs.add_chunks(embedder=embedder, batch_size=batch_size)

