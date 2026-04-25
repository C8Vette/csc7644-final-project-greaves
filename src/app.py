from __future__ import annotations

import streamlit as st

from answer import answer_query
from chunk_embed import ensure_chroma_collection

'''
Streamlit frontend for BoostRAG

This is supposed to be a simple UI interface for asking questions and displaying the
answers along with their sources for testing and debugging the RAG pipeline.
'''
st.set_page_config(
    page_title="BoostRAG",
    page_icon="🏎️",
    layout="centered",
)

@st.cache_resource
def initialize_vectors() -> None:
    """
    Initialize the Chroma vector database with embedded chunks.

    This function ensures that the Chroma collection is created and populated with
    the necessary data. It is cached so that it doesn't have to reinitialize constantly.
    """
    ensure_chroma_collection()

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #141b2d 0%, #0b1020 35%, #05070d 100%);
        color: #f5f7fa;
    }

    .main .block-container {
        max-width: 920px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #ffffff;
        letter-spacing: 0.3px;
    }

    p, label, .stMarkdown, .stCaption {
        color: #d7dbe3;
    }

    .boostrag-hero {
        padding: 1.5rem 1.5rem 1rem 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        background: linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.02) 100%);
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        margin-bottom: 1.5rem;
    }

    .boostrag-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }

    .boostrag-tagline {
        color: #ff5a5f;
        font-weight: 600;
        letter-spacing: 0.2px;
        margin-bottom: 0.8rem;
    }

    .boostrag-subtle {
        color: #aeb6c5;
        font-size: 0.98rem;
        line-height: 1.6;
    }

    .boostrag-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 1.1rem 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.22);
    }

    .boostrag-answer {
        font-size: 1.03rem;
        line-height: 1.7;
        color: #f5f7fa;
    }

    .boostrag-source {
        padding: 0.75rem 0.9rem;
        border-radius: 14px;
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0.75rem;
    }

    .boostrag-source-title {
        color: #ffffff;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .boostrag-source-meta {
        color: #9fb0c7;
        font-size: 0.92rem;
        margin-bottom: 0.35rem;
    }

    .stTextInput input {
        border-radius: 14px;
        border: 1px solid #2a3140;
        background-color: #101622;
        color: #ffffff;
    }

    .stTextInput input:focus {
        border-color: #ff5a5f;
        box-shadow: 0 0 0 1px #ff5a5f;
    }

    .stButton > button {
        border-radius: 14px;
        border: none;
        background: linear-gradient(90deg, #d72638 0%, #ff5a5f 100%);
        color: white;
        font-weight: 700;
        padding: 0.65rem 1.2rem;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #b81f2f 0%, #eb4f55 100%);
        color: white;
    }

    .stSlider label {
        color: #d7dbe3 !important;
    }

    .stExpander {
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        background-color: rgba(255,255,255,0.02);
    }

    a {
        color: #66b3ff !important;
    }

    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 1rem 0 1.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="boostrag-hero">
        <div class="boostrag-title">BoostRAG</div>
        <div class="boostrag-tagline">BMW M340i aftermarket parts research assistant</div>
        <div class="boostrag-subtle">
            Ask about intakes, downpipes, tunes, fitment, or product details.
            BoostRAG answers using only the retrieved corpus evidence.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

query = st.text_input(
    "Enter your question:",
    placeholder="Example: How much is a Dinan Stage 1 tune?",
)

top_k = st.slider(
    "Number of retrieved sources",
    min_value=1,
    max_value=5,
    value=2,
)

if st.button("Ask BoostRAG", type="primary"):
    if not query.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Retrieving evidence and generating answer..."):
            try:
                answer_text, chunks = answer_query(query.strip(), top_k=top_k)

                st.subheader("Answer")
                st.markdown(
                    f'<div class="boostrag-card boostrag-answer">{answer_text}</div>',
                    unsafe_allow_html=True,
                )

                st.subheader("Sources used")

                # Collect qunique sources so that the same file isn't shown mulitple times
                seen = set()
                source_blocks = []

                for chunk in chunks:
                    meta = chunk["metadata"]
                    source_file = meta.get("source_file", "unknown")
                    product = meta.get("product", "N/A")
                    category = meta.get("category", "N/A")
                    url = meta.get("url", "")

                    key = (source_file, product)
                    if key in seen:
                        continue
                    seen.add(key)

                    url_html = f'<a href="{url}" target="_blank">{url}</a>' if url else ""

                    source_blocks.append(
                        f"""
                        <div class="boostrag-source">
                            <div class="boostrag-source-title">{product}</div>
                            <div class="boostrag-source-meta">{source_file} • {category}</div>
                            <div>{url_html}</div>
                        </div>
                        """
                    )

                st.markdown(
                    f'<div class="boostrag-card">{"".join(source_blocks)}</div>',
                    unsafe_allow_html=True,
                )

                with st.expander("Debug: Retrieved chunks"):
                    for i, chunk in enumerate(chunks, start=1):
                        meta = chunk["metadata"]
                        st.markdown(f"### Chunk {i}")
                        st.write(f"**Source file:** {meta.get('source_file', 'unknown')}")
                        st.write(f"**Product:** {meta.get('product', 'N/A')}")
                        st.write(f"**Category:** {meta.get('category', 'N/A')}")
                        st.write(chunk["text"])

            except Exception as e:
                st.error(f"Something went wrong: {e}")