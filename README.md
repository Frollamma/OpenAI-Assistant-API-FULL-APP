# Introduction

This repo contains a simple OpenAI Assistant API GUI made with streamlit. It aims to simply the process of developing a GUI for an Assistant, in fact with this repo you don't to communicate directly with the Assistants API, it is fully handled by the app, the only thing you need is to provide the functions that the Assistant might call and return JSON.

## How it works

When a user chats with your Assistant, your Assistant might fire a [Function Call](https://platform.openai.com/docs/guides/function-calling), it means that it will generate a JSON containing the name of the function that it wants to call and its argument names and values. You can define your functions in the file `functions/main.py`, these functions will be imported and the app will automatically parse the JSON of the function call, correctly matching the function and its arguments. That's why you have to worry only about the functions implementation.

# Cloning as template

This repo is a template repository, it means that you can create a new repository with same files and structure of this one. Here is the `gh` command to create a public repository based on this repo

```sh
gh repo create Your-Repo-Name --public --template Frollamma/OpenAI-Assistant-API-UI
```

and to clone it you can use the following command

```sh
gh repo clone Your-Repo-Name
```

# Setup

First install the Python requirements.

```sh
pip install -r requirements.txt
```

Create a file called `secrets.toml` inside the `.streamlit` directory. This is the example file

```toml
CHATBOT_NAME = "Test"
OPENAI_API_KEY = "YOUR_API_KEY"
ASST_ID = "YOUR_ASSISTANT_ID"
```

# Run

```
streamlit run app.py
```

# Wanted features

- Add the possibility to use vanilla ChatGPT
- Add command line arguments
- Find something better than a folder named "functions"?
- Find a way to avoid name conflicts with file `functions/main.py` (they are very very unlucky, but possible)
- Add sidebar and chat history
- Add possibility to select different assistants
- Add support for more models available through API, like Gemini
- Add support for open source LLMs
