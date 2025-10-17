import json
from pathlib import Path
from time import time
from sentence_transformers import CrossEncoder
# import chromadb
from app.configs.config import rag_config
import psutil
from sklearn.preprocessing import normalize


#  FYTURE UPDATE 
# embeddings = model.encode(texts, convert_to_tensor=False)
# embeddings = normalize(embeddings)  # L2 normalize
def confidence_label(score):
    if score >= 0.9:
        return "🔥 Excellent"
    elif score >= 0.75:
        return "✅ Good"
    elif score >= 0.6:
        return "⚠️ Weak"
    else:
        return "❌ Irrelevant"
    
class QueryRag():
    def __init__(self, query,embedder,reranker, client, collection, n_result:int=5):
        self.start = time()
        self.n_result = n_result
        # self.embedder_model = rag_config['EMBEDDING_MODEL']
        self.query = query
        # self.collection_name = rag_config['COLLECTION_NAME']
        # chroma_client = chromadb.PersistentClient(path="data/embeddings")
        # print(f'*** Loading Embeding MOdel: {Path(self.embedder_model).name}')
        # self.embedder = SentenceTransformer(self.embedder_model)
        self.embedder = embedder
        self.reranker = reranker
        elapsed = time()
        # print(f'*** OADED SUCCESSFULY in {elapsed - self.start}: Embeding MOdel: {self.embedder_model}')
        # self.client = chromadb.PersistentClient(path=rag_config['EMBEDDING_FOLDER'])
        self.client = client
        # self.collection = self.client.get_or_create_collection(self.collection_name)
        self.collection = collection
        self.results = []
        print("Count: ", self.collection.count())
    
    def retrive(self):
        query_embedding = self.embedder.encode([self.query], normalize_embeddings=True)[0]  # [0] to get vector not list of list
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.n_result
            )
        self.results = results
        # self.query = query_embedding
        with open('app/logs/rag.json', 'w') as f:
            json.dump(results, f)
        # del self.embedder_model, self.embedder, self.collection, self.client, self.collection_name
        return results
    
    def rerank(self, query: str=None, docs:list=None):
        if not query:
            query = self.query
        if not docs:
            docs= self.results["documents"][0]
        # ---------------------------------------------
        if not self.results:
            print('no Result please Retrive First !!')
        else:
            scores = self.results["distances"]
            # del self.results
            print(f'*** Reranking {len(docs)} Results')
            # model = rag_config['RERANKER_MODEL']
            # model = 'models/base/reranker/arabic-reranker'
            # print(f'*** Model {Path(model).name} LOading ***')
            
            # print(f'*** Model {model} Loaded in {elapsed:.2f} SEC ***')
            pairs = [[query, d] for d in docs]
            start = time()
            scores = self.reranker.predict(pairs)
            # ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
            ranked = sorted([(doc, score) for doc, score in zip(docs, scores) if score >= rag_config['RAG_THRESHOLD']]
                            ,key=lambda x: x[1],reverse=True)
            elapsed = time() - start
            self.results = []
            for i, (doc, score) in enumerate(ranked, 1):
                print(f"{i}. Similarity: {score:.4f}")
                print(f"{confidence_label(score)} | {score:.4f}")
                print(f"Document: {doc[:200]}...")
                print("-" * 80)
                rank = {i:f'{score:.4f}', 'confidence_label':f'{confidence_label(score)} | {score:.4f}',
                        'document':f'{doc[:200]}...', 'end':'-'*80}
                self.results.append(rank)
                if not ranked:
                    print(f"No results above threshold ({rag_config['RAG_THRESHOLD']})")
            print(f'*** Reranking Successfully Finished in {elapsed:.2f}  Sec')
            
            

    
    def report_retrieval(self, model_name_or_path="./models/base/embedding/bge-m3"):
        print("\n==============================")
        print("🔍 RETRIEVAL REPORT")
        print("==============================")

        # --- Tokenization Info ---
        tokenizer = self.embedder.tokenizer
        tokens = tokenizer.tokenize(self.query)
        token_ids = tokenizer.encode(self.query, add_special_tokens=False)
        print(f"🧩 Query: {self.query}")
        print(f"Tokens ({len(tokens)}): {tokens[:15]}{'...' if len(tokens) > 15 else ''}")
        print(f"Token IDs count: {len(token_ids)}")

        # --- Memory Snapshot ---
        mem_before = psutil.virtual_memory().used / (1024**2)
        start = time()
        self.retrive()
        elapsed = time() - start
        mem_after = psutil.virtual_memory().used / (1024**2)
        mem_delta = mem_after - mem_before

        # --- Print Results ---
        for doc, score , metas in zip(self.results["documents"][0], self.results["distances"][0],self.results['metadatas'][0]):
            print(f"\nSimilarity: {score:.4f}")
            print(f"\nMEta: {metas}")
            print(f"Document: {doc[:600]}...")
            print("-" * 80)

        print(f"\n⏱ Retrieval Time: {elapsed:.4f} sec")
        print(f"💾 Memory Δ: {mem_delta:.1f} MB")
        print(f"📏 Tokens: {len(token_ids)}")
        print(f"📚 Model: {model_name_or_path}")
        print("==============================")

# retrieved = list(zip(docs, scores))
# retrieved = [(d, s) for d, s in retrieved if s >= 0.65]
# retrieved = sorted(retrieved, key=lambda x: x[1], reverse=True)

# # Only rerank top-N high-confidence
# rerank_candidates = [d for d, s in retrieved[:5]]
