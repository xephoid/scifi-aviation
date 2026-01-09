import chromadb
import ollama
import pypdf
import yaml
from sys import argv

if len(argv) < 3:
    print("Usage: python abstract_plan_execution.py <pdf_filename> <yaml_filename>")
    exit(1)

pdf_filename = argv[1]
yaml_filename = argv[2]
rules = ""

# Read PDF
with open(pdf_filename, "rb") as f:
    pdf = pypdf.PdfReader(f)
    for page in pdf.pages:
        rules += page.extract_text()

# Read YAML config
with open(yaml_filename, "r") as f:
    config = yaml.safe_load(f)

system_prompt_template = config["system_prompt"]
phases = config["phases"]

model = "gpt-oss:20b"
chroma_client = chromadb.PersistentClient()
collection = chroma_client.get_or_create_collection("bgtest")

ollama_client = ollama.Client()

history = []

# Prepare system prompt
prompt = system_prompt_template.replace("{rules}", rules).replace("{steps}", "\n".join([str(index + 1) + ". " + phase["name"] for index, phase in enumerate(phases)]))
history.append({"role": "system", "content": prompt})

# Execute phases
for index, phase in enumerate(phases):
    relevantDocuments = collection.query(
        query_texts=[phase["prompt"]],
        n_results=3,
    )
    print(relevantDocuments["ids"])
    history.append({"role": "user", "content": "Here are some relevant documents for this next step:\n\n" + "\n\n".join(relevantDocuments["documents"][0])})
    history.append({"role": "user", "content": config["promptPrefix"] + phase["name"] + config["promptSuffix"] + phase["prompt"] + phase["promptDetails"] })
    
    response = ollama_client.chat(
        model=model,
        messages=history,
    )
    print(response["message"]["content"])
    phases[index]["plan"] = response["message"]["content"]
    history.append({"role": "assistant", "content": response["message"]["content"]})

# Write output
if config["output"]["type"] == "file":
    with open(config["output"]["filename"], "w", encoding="utf-8") as f:
        f.write("\n\n".join([phase["plan"] for phase in phases]))
if config["output"]["type"] == "console":
    print("\n\n".join([phase["plan"] for phase in phases]))
if config["output"]["type"] == "chroma":
    collection.add(
        ids=[phase["name"] for phase in phases],
        documents=[phase["plan"] for phase in phases],
        metadatas=[{"phase": phase["name"]} for phase in phases],
    )