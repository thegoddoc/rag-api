import os, re
import fitz
from langdetect import detect, DetectorFactory
from configs.config import rag_config
# -----------------------------
# Utility Functions
# -----------------------------
MAX_TOKENS = rag_config['MAX_TOKENS']
OVERLAP_TOKENS = rag_config['OVERLAP_TOKENS']

def normalize_arabic(text: str) -> str:
    """Normalize Arabic text for consistent embeddings and retrieval."""
    # Remove diacritics
    text = re.sub(r"[\u0617-\u061A\u064B-\u0652]", "", text)
    # Normalize common letter variants
    text = re.sub(r"[إأآا]", "ا", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"ؤ", "و", text)
    text = re.sub(r"ئ", "ي", text)
    text = re.sub(r"ة", "ه", text)
    # Remove tatweel (ـ)
    text = re.sub(r"ـ", "", text)
    # Normalize Arabic numerals to Western digits
    text = re.sub(r"[٠-٩]", lambda x: str(ord(x.group()) - 1632), text)
    # Remove punctuation, Latin symbols, and extra spaces
    text = re.sub(r"[^ء-ي0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def pdf_to_text(pdf_path):
    """Convert PDF to raw text using PyMuPDF."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            page_text = page.get_text()
            text += page_text + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def clean_text(text):
    """Basic cleaning: remove multiple spaces, page headers/footers."""
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\s*Page\s+\d+',' ', text)
    text = text.strip()
    return text

def chunk_text_auot(text,tokenizer,  max_tokens=700, overlap=OVERLAP_TOKENS):
    """Split text into overlapping chunks based on token count."""
    tokens = tokenizer.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += max_tokens - overlap
    return chunks

def chunk_text(text,tokenizer, max_tokens=MAX_TOKENS, overlap=OVERLAP_TOKENS):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    for i in range(0, len(tokens), max_tokens - overlap):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)
    return chunks

DetectorFactory.seed = 0  # ensures consistency across runs
def detect_file_language(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    try:
        lang = detect(text)
        return lang  # e.g. "ar", "en"
    except:
        return "unknown"