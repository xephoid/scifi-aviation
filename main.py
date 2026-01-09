import ollama
import chromadb

model = "qwen2.5-coder:7b"
chroma_client = chromadb.PersistentClient()
collection = chroma_client.get_or_create_collection("bgtest")

ollama_client = ollama.Client()

gameName = "Agent Hunter"
developmentPrompts = [
    "Write the " + gameName + "Game.js file for a " + gameName + " game. This is the game object that will be passed to the boardgame.io Client",
    "Write the App.css file for a " + gameName + " game.",
    "Write the " + gameName + "Board.jsx file for a " + gameName + " game. This is the board object that will be passed to the boardgame.io Client",
    # "Write the App.jsx file for a " + gameName + " game. It should initialize the Client with the game and board objects. You can assume there files called " + gameName + "Game.js and " + gameName + "Board.js which contain the game and board objects respectively.",
]

# query = input(">>>")
history = [
    {"role": "system", "content": "You are a javascript game developer. You will use React and boardgame.io for this task. You do not include any other external libraries. Your code will be complete and ready to use. No TODOs or placeholder comments. Here are the relevant documents and files you need to complete this task:"},
]

for prompt in developmentPrompts:
    releventCode = collection.query(
        query_texts=[prompt],
        n_results=5,
    )

    print("\n\nUser Prompt: " + prompt)
    print(releventCode["ids"])

    print("\n\n\n")

    history.append({"role": "system", "content": releventCode["documents"][0][0]})
    history.append({"role": "system", "content": releventCode["documents"][0][1]})
    history.append({"role": "system", "content": releventCode["documents"][0][2]})
    history.append({"role": "system", "content": releventCode["documents"][0][3]})
    history.append({"role": "system", "content": releventCode["documents"][0][4]})
    history.append({"role": "user", "content": prompt + "\n\n" + "CHECK FOR COMPLETENESS: Are there any TODOs or placeholders in the code? Please respond with only the code you need to complete this task. Do not include any additional text."})

    done = False
    response = ""
    tries = 0
    while not done:
        response = ollama_client.chat(
            model=model,
            messages=history,
        )

        reviewResponse = ollama_client.chat(
            model=model,
            messages=[
                {"role": "system", "content": "You are a javascript code reviewer. You evaluate the code for completeness and correctness. You only respond yes or no."},
                {"role": "user", "content": "Is the code free of placeholders and TODOs? Meaning there are no comments like '// Implementation logic for ...' or // 'Render player info here'.\n\nPlease respond with only yes or no." + "\n\n" + response["message"]["content"]}
            ],
        )

        if "yes" in reviewResponse["message"]["content"] or "Yes" in reviewResponse["message"]["content"]:
            done = True
        else:
            tries += 1
            print("Review response: " + reviewResponse["message"]["content"])
            print("Review failed, trying again...")
            if tries > 5:
                print("Failed to complete code after 5 tries")
                done = True

    print(response["message"]["content"])
    history.append({"role": "assistant", "content": response["message"]["content"]})
