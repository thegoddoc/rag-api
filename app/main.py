import sys
import uvicorn 
from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from configs.config import rag_config
from scripts.query_rag import QueryRag
from scripts.pydant import QueryRequest, QueryMode


app = FastAPI(title="RAG FastAPI Demo")
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
    qr = QueryRag(query.query, query.k)
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


    