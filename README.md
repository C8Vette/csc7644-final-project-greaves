# BoostRAG

BoostRAG is a retrieval augmented generation (RAG) assistant for researching BMW M340i aftermarket performance parts. It was built as the final project for **CSC 7644: Applied LLM Development**.

## Project Overview

BoostRAG helps users ask questions about BMW M340i aftermarket parts using a manually curated corpus of product pages, fitment notes, and tuning-related resources. The goal is to provide grounded answers tied to retrieved evidence rather than hallucinated responses from a generic LLM.

This project focuses on a small, realistic prototype rather than a large-scale automotive search engine. The current system is scoped around one vehicle platform and a limited set of modification categories such as intakes, downpipes, and tunes.

Live demo: https://boostrag.streamlit.app

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

### Configure Environment Variables
Create a `.env` file in the project root and add:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Install Dependencies
From the project root, run:

```bash
pip install -r requirements.txt
```

## Running the application

### Step 1: Building the vector store
Run the following command to build the Chroma database with
the current data sources:

```bash
python src/chunk_embed.py
```

### Step 2: Launch the Streamlit App
Run the following command to start the app:

```bash
python -m streamlit run src/app.py
```

### Note:
If Streamlit is waking from sleep, the first load may take a few moments. Refresh the page if the 
interface does not appear after startup.

Additionally I deployed this app through streamlit, to access
the Deployed version, you need only visit `boostrag.streamlit.app`.

## Using The App

### How to use BoostRAG
1. Launch the app locally or open the deployed version at `boostrag.streamlit.app`. Once a new tab
opens if running locally, be sure to reload the tab for safety in the event nothing loads initially.

2. Enter a question about aftermarket or performance parts regarding the BMW M340i in the text box.

3. Adjust the slider choose how many retrieved sources you want to use as supporting evidence for the
question.

4. Click "Ask BoostRAG" to generate a response.

5. Check the answer you got.

6. Check the "Sources Used" and debug section to see which corpus sources were used to answer your question.

7. Expand the "Debug" area to see what raw data was used.

### Example Questions
- How much is a stage 1 Dinan tune?
- Which intake mentions sound improvement?
- Which downpipe mentions gains with a tune?
- Does any source mention warranty restrictions?
- Which products fit the BMW G20 M340i?

  *Out Of Context question*
- When will Jon Snow get his own spinoff show from Game of Thrones?

### Expected Behaviors
By design, BoostRAG only answers based on the sources from its corpus (located in data/cleaned). If the corpus
does not contain the relevant information to answer a question, it should reject it and tell you something akin to
"I lack the relevant information to answer this questions". It will use what it has to attempt to answer an
unrelated, yet somewhat familiar question, but it will ultimately refuse. A question you can test this with is,
"What Turbo upgrade options are available for the m340i?" Turbos use very similar language to some of the other 
parts included in the corpus, but there is no evidence pertaining to Turbos themselves, the model will recognize this
after exploring sources almost in the same domain, and let the user know that it lacks the evidence. When it comes to 
completely irrelevant questions such as questions about tv shows, the model will reject entirely.


## Repository Organization

- `src/` - main application code for BoostRAG's RAG pipeline and interface
    - `answer.py` – builds the evidence context and generates grounded answers from retrieved chunks
    - `app.py` – Streamlit front end for interacting with BoostRAG
    - `chunk_embed.py` – chunks cleaned corpus documents, generates embeddings, and stores them in ChromaDB
    - `preprocess.py` – loads and parses cleaned corpus text files
    - `retrieve.py` – retrieves top-k relevant chunks from the vector database

- `data/` – project data used by the retrieval pipeline
    - `cleaned/` – cleaned corpus text files used for retrieval

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
