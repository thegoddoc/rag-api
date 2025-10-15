import yaml
from pathlib import Path

# Base directory = project root (parent of "app")
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

config = yaml.safe_load(open(Path(__file__).resolve().parents[1] / "configs/config.yaml"))
rag_config = yaml.safe_load(open(Path(__file__).resolve().parents[1] / "configs/rag_config.yaml"))
rag_config['EMBEDDING_FOLDER'] = DATA_DIR/'embeddings'
rag_config['INPUT_FOLDER'] = DATA_DIR/'raw'
rag_config['OUTPUT_FOLDER'] =DATA_DIR/'processed'
agent_config = yaml.safe_load(open(Path(__file__).resolve().parents[1] / "configs/agent_config.yaml"))
tokenizer_config = yaml.safe_load(open(Path(__file__).resolve().parents[1] / "configs/tokenizer_config.yaml"))
training_config = yaml.safe_load(open(Path(__file__).resolve().parents[1] / "configs/training_config.yaml"))

