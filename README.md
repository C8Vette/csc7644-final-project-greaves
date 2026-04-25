# BoostRAG

BoostRAG is a retrieval augmented generation (RAG) assistant for researching BMW M340i aftermarket performance parts. It was built as the final project for **CSC 7644: Applied LLM Development**.

## Project Overview

BoostRAG helps users ask questions about BMW M340i aftermarket parts using a manually curated corpus of product pages, fitment notes, and tuning-related resources. The goal is to provide grounded answers tied to retrieved evidence rather than hallucinated responses from a generic LLM.

This project focuses on a small, realistic prototype rather than a large-scale automotive search engine. The current system is scoped around one vehicle platform and a limited set of modification categories such as intakes, downpipes, and tunes.

## Key Features / Capabilities

- Answers questions over a custom BMW M340i corpus using a RAG pipeline
- Retrieves relevant source chunks from a Chroma vector database
- Generates grounded answers using OpenAI models
- Displays supporting sources in a Streamlit interface
- Refuses when the corpus does not contain sufficient evidence
- Supports a modular workflow with separate preprocessing, embedding, retrieval, and answer-generation components

## Tech Stack and Architecture (High-Level)

### Core Technologies
- **Python**
- **OpenAI API** for embeddings and response generation
- **ChromaDB** for vector storage and retrieval
- **Streamlit** for the web interface

### High-Level Architecture
BoostRAG uses a standard RAG workflow:

1. Clean corpus documents are stored in `data/cleaned/`
2. Documents are parsed and chunked into smaller sections
3. Each chunk is embedded using OpenAI embeddings
4. Embeddings and metadata are stored in ChromaDB
5. A user query is embedded and matched against stored chunks
6. Top-k retrieved chunks are passed to the LLM
7. The LLM generates a grounded answer and shows supporting sources

## Setup Instructions

### Prerequisites
- Python 3.10+ recommended
- Built on Windows
- `pip` installed and available
- OpenAI API key

### Install Dependencies
From the project root, run:

```bash
pip install -r requirements.txt
```

## Running the application

### Step 1: Building the vector store
After adding anymore cleaned corpus files to the 'data/cleaned/' folder, you have
to build the store by running the following command:

```bash
python src/chunk_embed.py
```

### Step 2: Launch the Streamlit App
Run the following command to start the app:

```bash
python -m streamlit run src/app.py
```

## Repository Organization

- `src/` - main applciation code for BoostRAG's rag pipeline and interface
    - `answer.py` – builds the evidence context and generates grounded answers from retrieved chunks
    - `app.py` – Streamlit front end for interacting with BoostRAG
    - `chunk_embed.py` – chunks cleaned corpus documents, generates embeddings, and stores them in ChromaDB
    - `preprocess.py` – loads and parses cleaned corpus text files
    - `retrieve.py` – retrieves top-k relevant chunks from the vector database

- `data/` – project data used by the retrieval pipeline
    - `cleaned/` – cleaned corpus text files used for retrieval

- `tests/` – reserved for evaluation scripts or future automated tests

- `vectorstore/` – local ChromaDB storage artifacts generated during indexing  
    - This directory is used at runtime and is ignored in Git

- `requirements.txt` – Python dependencies required to run the project

- `README.md` – project documentation, setup instructions, and usage guide

- `.env.example` – example environment variable file showing required API key format

The goal of this structure is to make it easy for a grader to quickly locate the main code, data, and retrieval components.

## Attributions and Citations

This project wouldn't have been possible without the following resources:
- OpenAI API documentation
- Chroma documentation
- Streamlit documentation
- Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*

External code adaptation:
- Some implementation patterns were adapted from official documentation and examples for OpenAI embeddings, ChromaDB usage, and Streamlit app structure.
- No external GitHub repository was copied wholesale into this project.