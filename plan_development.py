import chromadb
import ollama
import pypdf
from sys import argv

filename = argv[1]
rules = ""

with open(filename, "rb") as f:
    pdf = pypdf.PdfReader(f)
    for page in pdf.pages:
        rules += page.extract_text()

model = "gpt-oss:20b"
chroma_client = chromadb.PersistentClient()
collection = chroma_client.get_or_create_collection("bgtest")

ollama_client = ollama.Client()

planningPhases = [
    {
        "name": "Setup Steps and Initial Player Decisions",
        "prompt": "Think about the setup steps and initial player decisions. Boardgame.io has a built-in system for managing setup steps and initial player decisions. List every possible decision a player can make. How should this player interface be designed?"
    },
    {
        "name": "Player Interaction Points",
        "prompt": "Think about the player interaction points. List every possible action a player can take. How should the player interface be designed?"
    },
    {
        "name": "Public vs Private Information",
        "prompt": "Think about the public vs private information. Boardgame.io has a built-in system for managing public and private information. What information is visible to all players? What information is only visible to the player? How should it be displayed? What about when player information is revealed to other players?"
    },
    {
        "name": "Phase Structure",
        "prompt": "Think about the phase structure. Boardgame.io has a built-in system for managing phases and turns. Identify the structure of phases and turns."
    },
    {
        "name": "Move Implementation",
        "prompt": "Think about the move implementation. Boardgame.io has a built-in system for managing moves and actions. Describe how each move should be implemented"
    },
    {
        "name": "Game Screens",
        "prompt": "Think about the game screens. Describe the game screens and transitions between them"
    },
    {
        "name": "Network Implementation",
        "prompt": "Think about the network implementation. Boardgame.io has a built-in network implementation. Describe how to implement it"
    },
    {
        "name": "AI Player Implementation",
        "prompt": "Think about the ai player implementation. Boardgame.io has a built-in ai player. Describe how to implement it"
    }
]

history = []

with open("../DEVELOPMENT_PLAN_PROMPT.md", "r") as f:
    prompt = f.read()
    prompt = prompt.replace("{rules}", rules)
    
    history.append({"role": "system", "content": prompt})

for index, phase in enumerate(planningPhases):
    relevantDocuments = collection.query(
        query_texts=[phase["prompt"]],
        n_results=3,
    )
    print(relevantDocuments["ids"])
    history.append({"role": "user", "content": "Here are some relevant documents for this next step:\n\n" + "\n\n".join(relevantDocuments["documents"][0])})
    history.append({"role": "user", "content": "Write the " + phase["name"] + " section for the game. " + phase["prompt"] + ". Your response should be exhaustive. Keep in mind the developer will be using React and boardgame.io to implement the game. Do not include plans for other phases. Also, do not include 'Nice to have' features. Only features explaned in the rules." })
    
    response = ollama_client.chat(
        model=model,
        messages=history,
    )
    print(response["message"]["content"])
    planningPhases[index]["plan"] = response["message"]["content"]
    history.append({"role": "assistant", "content": response["message"]["content"]})

with open("planning.md", "w", encoding="utf-8") as f:
    f.write("\n\n".join([phase["plan"] for phase in planningPhases]))