import os, re, glob, json
import fitz 
from tqdm import tqdm
from time import time
from app.configs.config import *
from app.scripts.pre_utills import *
from sentence_transformers import SentenceTransformer
from typing import List

OUTPUT_FOLDER = rag_config['OUTPUT_FOLDER']
model_name = rag_config['EMBEDDING_MODEL']
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

class Preprocess():
    def __init__(self, INPUT_FOLDER:str):
        print(f'PREPROCEssing *** OutputFOlder : {OUTPUT_FOLDER}')
        print(f'\n Starting PreProcessing of Data in DIrectory:{INPUT_FOLDER}\n')
        self.all_files = []
        self.input_directory = INPUT_FOLDER
        print(f'*** Loading Tokenizer ***')
        self.tokenizer = SentenceTransformer(model_name).tokenizer
        self.config = rag_config
        
    # Read files
    def files(self, all: int=1): # 0=Fslse 1=True
        if all == 1:
            self.all_files = glob.glob(os.path.join(self.input_directory,"**", "*"), recursive=True)
            print(f"Found {len(self.all_files)} files.")
            
        else:
            pass
        return self.all_files

    # Clean Text 
    def Split_file_to_chunks(self):
        time_per_item = [] # 0 for id , 1 dor elapsed time 
        if len(self.all_files)== 0:
            self.all_files = self.files(1)
        skipped_files = []
        chunk_counter = 0
        for file_path in tqdm(self.all_files):
            ext = Path(file_path).suffix.lower()
            # Determine category from folder structure or filename
            if 'medical_cases' in str(Path(file_path)):
                category = f'medical_cases'
                topic = f'{Path(file_path).parent.name}'
                # print('Medical_cases: ', Path(file_path), '  >', category)
            elif 'products' in str(Path(file_path)):
                category = f'products'
                topic = f'{Path(file_path).parent.name}'
                # print('products: ', Path(file_path), '  >', category)
            else:
                category = Path(file_path).parent.name
                topic = category
            if ext == ".pdf":
                text = pdf_to_text(file_path)
            elif ext in [".txt", ".md"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            else:
                print(f"Skipping unsupported file: {file_path}")
                skipped_files.append(file_path)
                continue
            #  Normalize text 
            text = clean_text(text)
            print(f'Text CLeaned')
            
            try:
                language = detect(text)
            except Exception as e:
                print(f"ERROR: {e}")
                language = 'un'
            #  MAke Sure Language is Arabic or English Only
            if language in ['ar', 'en']:
                if language == 'ar':
                    text = normalize_arabic(text)
                    print("TEXT ARABIC NORMALIZED")
            else:
                continue
            #  Split file to Chunks
            start = time()
            print(f"*** Start CHUNKING OF FILE ({file_path})")
            chunks = chunk_text(text, tokenizer=self.tokenizer)
            # Add Attributes and Metadate to chunk
            for i, chunk in enumerate(chunks):
                chunk_data = {
                    "id": f"{Path(file_path).stem}_chunk{i}",
                    "text": chunk,
                    "source_file": file_path,
                    "category": category,
                    "topic":topic,
                    "language": language,
                    "tokens": len(self.tokenizer.encode(chunk))
                }
                #  Export chunks to jason files in preprocessed 
                out_path = os.path.join(OUTPUT_FOLDER, f"{chunk_data['id']}.json")
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(chunk_data, f, ensure_ascii=False, indent=2)
                chunk_counter += 1
                elapsed = round(time() - start)
                print(f"the Chunk {i} for: {file_path} toke: {elapsed}")
                time_per_item.append([id, elapsed])  
        print(f"Created {chunk_counter} chunks in {OUTPUT_FOLDER}.")
        
        return {"time_per item": time_per_item}
    def log_processed_files(self):
        with open(rag_config['PROCESSED_FILES'],'r') as f:
            lst = json.load(f)
        names = [Path(file).name for file in self.all_files if Path(file).is_file()]
        with open(rag_config['PROCESSED_FILES'], 'w') as f:
            json.dump(names, f)
        print(f"ProCessed: {len(names)} Files Logged  to {rag_config['PROCESSED_FILES']}.")  

    def del_all_files(self):
        file_list = [file for file in self.all_files if Path(file).is_file()]
        for file_name in file_list:
            # Create a Path object
            file_path = Path(file_name)
            try:
                # The `unlink()` method deletes the file
                # The `missing_ok=True` argument prevents an error if the file doesn't exist
                file_path.unlink(missing_ok=True)
                print(f"Deleted {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

if __name__ == '__main__':
    OUTPUT_f = os.join("./data/raw/", 'products')
    print(OUTPUT_f)
    files = Preprocess('data/raw').files()
    print(files)