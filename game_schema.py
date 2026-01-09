import ollama
import pypdf
from sys import argv
import json

# gpt-oss:20b
# llama3.2:3b
model = "llama3.2:3b"

ollama_client = ollama.Client()

schemaSections = {
    "top level": {"prompt": "This should contain the name, objective, player count range, and any other top level information about the game. It should not include any of the other sub sections like phases, moves, setup, components, keywords, rulesNotes, or gameState."},
    "phases": {"prompt": "There should at leaset be a 'Setup', 'Player Turn', and 'End Game' phase. Some games may have additional phases or describe the phases differently. Use the names that the rulebook uses if provided."},
    "moves": {"prompt": "This list should contain every move or action a player can take."},
    "setup": {"prompt": "This list should contain every setup step necessary to start the game."},
    "components": {"prompt": "This list should contain every component used in the game."},
    "keywords": {"prompt": "This list should contain every keyword specified in the rulebook."},
    "rulesNotes": {"prompt": "This list should contain any special rules or clarifications specified in the rulebook."},
    "gameState": {"prompt": "This data object should detail every state variable to be used in the game."},
}
filename = argv[1]
rules = ""
with open(filename, "rb") as f:
    pdf = pypdf.PdfReader(f)
    for page in pdf.pages:
        rules += "\n\n" + page.extract_text()

history = []

with open("../SCHEMA_PROMPT.md", "r") as f:
    prompt = f.read()
    prompt = prompt.replace("{rulebook}", rules)
    
    history.append({"role": "system", "content": prompt})
    
for section in schemaSections:
    history.append({"role": "user", "content": "Write the " + section + " json section for the game. " + schemaSections[section]["prompt"] + ". Your response should be exhaustive. Please respond in json format. Do not include any additional text." })
    
    done = False
    while not done:
        response = ollama_client.chat(
            model=model,
            messages=history,
        )
        
        try:
            rawJson = response["message"]["content"].replace("```json", "").replace("```", "")
            if section == "top level":
                schemaSections[section]["json"] = json.loads(rawJson)
            else:
                schemaSections[section]["json"] = json.loads(rawJson)[section]
            print(rawJson)
            history.append({"role": "assistant", "content": response["message"]["content"]})
            done = True
        except:
            print("Invalid json!")
            print(response["message"]["content"])

final = schemaSections["top level"]["json"]
for section in schemaSections:
    if section == "top level":
        continue
    final[section] = schemaSections[section]["json"]

print("\n\n----------------------------------------------------------------------")
print(final)

with open(final["name"] + "_schema.json", "w") as f:
    json.dump(final, f, indent=4)

