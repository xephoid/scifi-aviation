import chromadb
import os

chroma_client = chromadb.PersistentClient()
# chroma_client.reset()
collection = chroma_client.create_collection("bgtest")
onlyFileTypes = [".ts", ".js", ".md", ".json", ".html", ".css", ".py"]
print("Looking...")
for subdir, dirs, files in os.walk("C:/Users/zekes/Code/boardgame.io"):
    for file in files:
        if not file.endswith(tuple(onlyFileTypes)):
            continue
        print(os.path.join(subdir, file))
        id = os.path.join(subdir, file)
        with open(os.path.join(subdir, file), "r", encoding="utf-8") as f:
            content = "".join(f.readlines())
            # print(content)
            collection.add(
                documents=[content],
                ids=[id],
            )