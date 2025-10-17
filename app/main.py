import sys, os
import gc
import uvicorn 
from time import time
from fastapi import FastAPI, BackgroundTasks, UploadFile, File,HTTPException
from threading import Thread
from contextlib import asynccontextmanager

from app.configs.config import rag_config
from app.scripts.query_rag import QueryRag
from app.scripts.build_index import VectoreStore
from app.scripts.preprocess import Preprocess
from app.scripts.pydant import QueryRequest, QueryMode, IngestRequest
from app.api import upload



def load_resources():
    from sentence_transformers import SentenceTransformer, CrossEncoder
    import chromadb
    global embedder, client, collection, reranker
    embedder = SentenceTransformer(embedder_model)
    client = chromadb.PersistentClient(path=rag_config['EMBEDDING_FOLDER'])
    collection = client.get_or_create_collection(collection_name)
    model = rag_config['RERANKER_MODEL']
    start_ = time()
    reranker = CrossEncoder(model)
    elapsed = time() - start_
    print(f'*** Model {model} Loaded in {elapsed:.2f} SEC ***')
    elapsed = time() - start
    print(f"✅ Models ready! IN {elapsed:.2f} Sec")

#  ----- START UP ------------
# @app.on_event("startup")
# def startup_event():
#     thread = Thread(target=load_resources, daemon=True)
#     thread.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global embedder, client, collection, reranker
    # Load the ML model
    thread = Thread(target=load_resources, daemon=True)
    thread.start()
    yield
    # Clean up the ML models and release the resources
    print("🧹 Cleaning up...")
    del embedder, client, collection, reranker
    gc.collect()


start = time()
embedder_model = rag_config['EMBEDDING_MODEL']
collection_name = rag_config['COLLECTION_NAME']
embedder = None
client = None
collection = None
reranker = None

app = FastAPI(title="RAG FastAPI Demo", lifespan=lifespan)
app.include_router(upload.router)

# Open log file in append mode (so logs stack)
# log_file = open("app.log", "a")
# err_file = open('err.log', "a")

# Redirect all prints to the file
# sys.stdout = log_file
# sys.stderr = log_file  # (optional) also capture errors

# ---------- Endpoints ----------
@app.get("/")
def welcome():
    # run indexing in background so API returns fast
    return {"message":"🚀 Welcome to your FastAPI RAG app!"}
# ----------- RAG --------------
@app.post("/query")
async def rag(query:QueryRequest, mode:QueryMode):
    i = '.'
    while not embedder or not collection or not client or not embedder_model or not collection_name:
        for i in range(4):
            print(f'\r LOADING: {"."*i}',end=' ')
    print(f'EMBEDDER NOT READY yet')

    qr = QueryRag(query.query,embedder=embedder,
                   client=client, 
                   collection=collection,
                    reranker=reranker,
                   n_result=query.k
                   )
    mode = mode.moode
    if mode=='retrive':
        qr.retrive()
    elif mode =='rerank':
        qr.retrive()
        qr.rerank()
    elif mode == 'report':
        qr.report_retrieval()
    res = qr.results
    return {"Rssults": res}


@app.post('/ingest')
async def ingest(req:IngestRequest, background_tasks:BackgroundTasks):
    # background_tasks.add_task(index_document, req.title, req.text, req.metadata)
    background_tasks.add_task(build_index, req.batch_size)
    return {"status":"accepted", "BATCH SIZE: ": req.batch_size}
    # VectoreStore

def build_index(batch_size:int):
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

@app.post("/process")
async def preprocess(background_tasks:BackgroundTasks):
    pr = Preprocess(INPUT_FOLDER=rag_config['INPUT_FOLDER'], embedder=embedder)
    background_tasks.add_task(pr.Split_file_to_chunks)
    files= pr.all_files()
    print(f'\n*** {{len(files)}} FILE PROCESSING STARTED\n')
    return {"status":f"{{len(files)}} FILE PROCESSING STARTED", "BATCH SIZE: ": len(files)}
    


if __name__ == '__main__':
    # uvicorn.run(app,
                # host='0.0.0.0',
                # port='8000',
                # reload=True
                # )
    print('RAG CONFIG: ',rag_config)
    q = 'panadol'
    qr = QueryRag(q)
    qr.report_retrieval()
    res = qr.results
    print(res)


    