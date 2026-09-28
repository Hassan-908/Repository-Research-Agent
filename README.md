# Repository Research Agent

A lightweight GitHub repository research agent built with **LangChain, Groq, FastAPI, and Streamlit**.

The agent researches GitHub repositories through the GitHub REST API, selects the tools required for the user's question, and generates a concise technical summary.

## Screenshots

### Streamlit Interface

<img width="964" height="415" alt="image" src="https://github.com/user-attachments/assets/2028acad-335c-4565-8f09-85ceb9b16fd2" />


### FastAPI Swagger Documentation

<img width="840" height="712" alt="image" src="https://github.com/user-attachments/assets/7fbde4fa-04c2-4981-8203-a3ec513347f6" />


## Features

- LangChain agent using `create_agent`
- Groq `openai/gpt-oss-20b`
- Automatic tool selection
- GitHub REST API integration
- Repository metadata analysis
- Programming language analysis
- Recent commit analysis
- FastAPI REST API
- Streamlit interface
- Error handling
- Displays tools used by the agent

## How It Works

```text
User Question
      ↓
LangChain Agent
      ↓
Select Required Tool(s)
      ↓
Python Tool
      ↓
GitHub REST API
      ↓
JSON Response
      ↓
Data Extraction
      ↓
Agent
      ↓
Groq LLM
      ↓
Technical Summary
```

The agent selects tools based on the question instead of calling every tool for every request.

For example:

```text
"What changed recently in facebook/react?"
                ↓
       get_recent_commits
                ↓
             Answer
```

A broader question can use multiple tools:

```text
"Give me a technical overview of facebook/react"
                ↓
     ┌──────────┼──────────┐
     ↓          ↓          ↓
 repository   languages  commits
     └──────────┼──────────┘
                ↓
        Technical Summary
```

## Available Tools

### `get_repository_info`

Retrieves repository metadata such as:

- Repository name
- Description
- Primary language
- Stars
- Forks
- Open issues
- Topics
- License
- Created date
- Updated date
- Default branch

### `get_repository_languages`

Retrieves the programming languages used by a repository and their byte counts through the GitHub Languages API.

### `get_recent_commits`

Retrieves the five most recent commits, including:

- Commit message
- Author
- Date
- Commit SHA
- Commit URL

## Tech Stack

- **Python**
- **LangChain**
- **Groq**
- **GPT-OSS 20B**
- **GitHub REST API**
- **Requests**
- **FastAPI**
- **Streamlit**

## Project Structure

```text
repository-research-agent/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── model.py
│   │
│   ├── tools/
│   │   └── github.py
│   │
│   ├── agent/
│   │   └── agent.py
│   │
│   ├── routes/
│   │   └── ask.py
│   │
│   └── main.py
│
├── streamlit_app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## API

The application exposes:

### `POST /ask`

Example request:

```json
{
    "question": "Give me a technical overview of facebook/react"
}
```

Example response:

```json
{
    "question": "Give me a technical overview of facebook/react",
    "answer": "React is a JavaScript library...",
    "tools_used": [
        "get_repository_info",
        "get_repository_languages",
        "get_recent_commits"
    ]
}
```

## Example Questions

```text
Analyze facebook/react
```

```text
What technologies does facebook/react use?
```

```text
What language does facebook/react mainly use?
```

```text
What changed recently in facebook/react?
```

```text
Show me the latest five commits from facebook/react.
```

```text
How many stars and forks does facebook/react have?
```

```text
Give me a complete technical overview of facebook/react.
```

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd repository-research-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`:

```env
GROQ_API_KEY=your_groq_api_key
GITHUB_TOKEN=
```

`GITHUB_TOKEN` is optional when working with public repositories.

### 5. Start FastAPI

```bash
uvicorn app.main:app --reload
```

Open the API documentation at:

```text
http://127.0.0.1:8000/docs
```

### 6. Start Streamlit

In another terminal:

```bash
streamlit run streamlit_app.py
```

## Error Handling

The application handles common failures including:

- Invalid repository names
- Repository not found
- Invalid GitHub credentials
- GitHub API errors
- API rate limiting
- Network errors
- Unexpected API responses
- Malformed JSON
- Missing environment variables

Errors are surfaced instead of being silently ignored.

## Project Purpose

This project demonstrates an LLM-powered agent that can interact with an external REST API through custom tools.

The core workflow is:

```text
LangChain Agent
      ↓
Tool Selection
      ↓
Python Function
      ↓
requests
      ↓
GitHub REST API
      ↓
JSON Data
      ↓
Data Extraction
      ↓
LLM
      ↓
Technical Summary
```

The project focuses on **agentic tool calling, REST API integration, structured data extraction, and LLM-based summarization** rather than RAG or vector databases.

## License

This project is intended for learning, experimentation, and portfolio demonstration.
