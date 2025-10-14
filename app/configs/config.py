import yaml
from pathlib import Path

config = yaml.safe_load(open(Path(__file__).resolve().parents[1] / "configs/config.yaml"))
rag_config = yaml.safe_load(open(Path(__file__).resolve().parents[1] / "configs/rag_config.yaml"))
agent_config = yaml.safe_load(open(Path(__file__).resolve().parents[1] / "configs/agent_config.yaml"))
tokenizer_config = yaml.safe_load(open(Path(__file__).resolve().parents[1] / "configs/tokenizer_config.yaml"))
training_config = yaml.safe_load(open(Path(__file__).resolve().parents[1] / "configs/training_config.yaml"))

