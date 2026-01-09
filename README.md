Messing around with local LLMs to see if I can get them to generate a functioning boardgame app.

This is probably my 4th iteration of this idea. I've tried a few different approaches and this is the most successful so far.

The plan is to use a local LLM to generate a plan for implementing a boardgame. Then I will use another local LLM to implement the plan.

The plan is generated using a YAML configuration file and a PDF of the rules. The plan is then executed using a Python script.

The plan is stored in a Chromadb database and can be used to implement the game.

YAML file format:

```yaml
system_prompt: "You are a professional game developer. You will be managing a developer who will be implementing the game. Here are the rules to the game:"

phases:
  - name: "Setup Steps and Initial Player Decisions"
    prompt: "Think about the setup steps and initial player decisions."
    
promptPrefix: "Write the "
promptSuffix: " section for the game."
promptDetails: ". Your response should be exhaustive. Keep in mind the developer will be using React and boardgame.io to implement the game. Do not include plans for other phases. Also, do not include 'Nice to have' features. Only features explaned in the rules."

output:
  type: "file or chromadb"
  filename: "planning.md" (if file)
  collection: "planning" (if chromadb)
```

The program will execute each prompt individually in the format:

```json
[
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": promptPrefix + prompt + promptSuffix + promptDetails
    }
]
```
It will do this for each phase of the plan retaining the history of the conversation. It also uses searches chromadb to find relevant code to include in the prompt.

Currently I have loaded the code from boardgame.io into chromadb.

To run the abstract planner:
```
py abstract_planner.py <rules.pdf> <phases.yaml>
```
LLMs tried so far:
- qwen2.5-coder:7b
- qwen2.5-coder:14b
- gpt-oss:20b
- llama3.2:3b
