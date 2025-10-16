import os
import json
from time import time
from tqdm import tqdm
from pathlib import Path
from scripts import logger
from scripts.logger import Logger
from configs.config import rag_config
import chromadb
from sentence_transformers import SentenceTransformer


mod_name = 'build_index'
processed_path = rag_config['OUTPUT_FOLDER']
#  store in chromadb
class VectoreStore():
    def __init__(self,embedder, client, collection_name:str,collection, vector_path):
        self.chunks = self.load_chunks(proceede_path=processed_path)
        self.embedder = embedder
        chroma_client = client
        self.collection = collection
        model_path = rag_config['EMBEDDING_MODEL']
        #  Future Replace split with Suffix os
        print(f'\n *** Start LOADING :  EMBEDDING_MODEL: {Path(model_path).name}')
        self.start = time()
        
        elapsed = time() - self.start
        print(f'\n *** EMBEDDING_MODEL: {Path(model_path).name} Loaded Successfully in {elapsed} SEC ***')
        
    ## try UPsert if is chunk
    #  
    # ## Add Chunk
    def add_chunks(self,embedder, chunks=None,  embeddings=None, batch_size:int=3, pr_path=processed_path):
        if chunks is None:
            chunks = self.chunks
        all_ids = chunks['ids'][:9]
        all_docs = chunks['docs']
        metadatas = chunks['metas']
        for i in tqdm(range(0, len(all_ids), batch_size)):
            batch_ids = all_ids[i:i + batch_size]
            batch_documents = all_docs[i:i + batch_size]
            batch_meta = metadatas[i:i+ batch_size]
            txt = "\n".join(batch_ids)
            print(f'\n *** Start EMBEDDING:  Batch_size: {batch_size} Documents:\n {txt}\n ')
            if embeddings is None:
                batch_embeddings = self.embed_chunks(embedder,batch_documents, batch_size)['embeddings']
            else:
                batch_embeddings = embeddings[i:i + batch_size] 
            print(f"\nIDS : {len(batch_ids)}, Docs : {len(batch_documents)}, Metas: {len(batch_meta)}")
            print(f'\n *** Start ADDING VECTORS TO VDB:  Batch_size: {batch_size}')
            self.collection.upsert(ids=batch_ids,
                           documents=batch_documents,
                           metadatas=batch_meta,
                           embeddings=batch_embeddings
                           )
        elapsed = time() - self.start
        print(f'**** REPORT:\n TOtal Time: {elapsed} \nTOtal Chunks: {len(chunks)} \nTOtal DIM : {len(batch_embeddings[0])}')
     
    def embed_chunks(self,embedder, chunks: list, batch_: int=3):
        embeddings = []
        time_for_embed = []
        # chunks = [chunk['text'] for chunk in chunks]
        em = 0
        start = time()
        for i,q in enumerate(chunks):
            embed = embedder.encode(q, normalize_embeddings=True, batch_size=batch_)
            embeddings.append(embed)
            elapsed = time() - start
            time_for_embed.append(elapsed)
            em += 1
            Logger(mod_name, [f'{em} Chunks embedded in {time_for_embed[-1]} SEC'])
        return {'embeddings':embeddings,'time_forembed': time_for_embed}
    
    def load_chunks(self, proceede_path):
        # Load processed JSON files
        print(f'loading ShUNKS from {Path(proceede_path).name}')
        processed_dir = rag_config['OUTPUT_FOLDER']
        all_ids = []
        all_docs = []
        metadatas=[]
        # all_embeddings = []
        #  9 batch for Testing **************
        for filename in tqdm(os.listdir(processed_dir)[:9]):
            if filename.endswith(".json"):
                with open(os.path.join(processed_dir, filename), "r", encoding="utf-8") as f:
                    doc = json.load(f)
                # print(doc)
                # add ids to list 
                all_ids.append(doc['id'])
                all_docs.append(doc['text'])
                # all_embeddings.append(np.array(doc["embedings"]))
                metadatas.append({"source": doc["source_file"],
                                  "category": doc["category"],
                                  "language": doc["language"],
                                  "tokens": doc["tokens"]
                                  })
        
        # print(f'DOcs: {doc}')
        # Add to vector store
        return {"ids":all_ids, "docs":all_docs, "metas":metadatas}
