import time
from pathlib import Path

import numpy as np
from google import genai
from google.genai import errors


DATA_DIR = Path("data")
RULES_PATH = Path("config/assistant_rules.md")

EMBEDDING_MODEL = "gemini-embedding-001"

MAX_RETRIES = 3
RETRY_DELAY = 2


def get_error_code(exc):
    return getattr(
        exc,
        "status_code",
        getattr(exc, "code", None),
    )


def load_rules():
    if not RULES_PATH.exists():
        raise FileNotFoundError(
            f"Assistant rules file not found: {RULES_PATH}"
        )

    rules = RULES_PATH.read_text(
        encoding="utf-8"
    ).strip()

    if not rules:
        raise ValueError(
            "Assistant rules file is empty."
        )

    return rules


def load_documents():
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"Data directory not found: {DATA_DIR}"
        )

    documents = []

    for path in sorted(DATA_DIR.rglob("*.md")):
        text = path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            continue

        documents.append(
            {
                "source": path.name,
                "text": text,
            }
        )

    if not documents:
        raise ValueError(
            "No Markdown documents were found "
            "in the data directory."
        )

    return documents


def split_by_headings(text):
    sections = []
    current_lines = []

    for line in text.splitlines():
        stripped = line.strip()

        is_heading = (
            stripped.startswith("#")
            and not stripped.startswith("```")
        )

        if is_heading and current_lines:
            section = "\n".join(
                current_lines
            ).strip()

            if section:
                sections.append(section)

            current_lines = [line]

        else:
            current_lines.append(line)

    if current_lines:
        section = "\n".join(
            current_lines
        ).strip()

        if section:
            sections.append(section)

    return sections


def split_large_section(
    text,
    chunk_size=1200,
    overlap=150,
):
    text = text.strip()

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError(
            "Chunk size must be greater than zero."
        )

    if overlap < 0:
        raise ValueError(
            "Chunk overlap cannot be negative."
        )

    if overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be smaller than chunk size."
        )

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = min(
            start + chunk_size,
            len(text),
        )

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def chunk_text(
    text,
    chunk_size=1200,
    overlap=150,
):
    text = text.strip()

    if not text:
        return []

    sections = split_by_headings(text)

    chunks = []

    for section in sections:
        chunks.extend(
            split_large_section(
                section,
                chunk_size=chunk_size,
                overlap=overlap,
            )
        )

    return chunks


def build_chunks():
    documents = load_documents()

    chunks = []

    for document in documents:
        document_chunks = chunk_text(
            document["text"]
        )

        for chunk in document_chunks:
            chunks.append(
                {
                    "source": document["source"],
                    "text": chunk,
                }
            )

    if not chunks:
        raise ValueError(
            "No text chunks were generated from "
            "the portfolio documents."
        )

    return chunks


def embed_single_text(
    client,
    text,
    max_attempts=MAX_RETRIES,
    retry_delay=RETRY_DELAY,
):
    text = text.strip()

    if not text:
        raise ValueError(
            "Cannot generate an embedding for empty text."
        )

    last_error = None

    for attempt in range(max_attempts):
        try:
            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text,
            )

            if (
                response is None
                or not response.embeddings
                or not response.embeddings[0].values
            ):
                raise ValueError(
                    "Embedding service returned an empty response."
                )

            return np.array(
                response.embeddings[0].values,
                dtype=np.float32,
            )

        except errors.ServerError as exc:
            last_error = exc
            code = get_error_code(exc)

            if (
                code in {500, 502, 503, 504}
                and attempt < max_attempts - 1
            ):
                time.sleep(retry_delay)
                continue

            raise

        except errors.ClientError as exc:
            last_error = exc
            code = get_error_code(exc)

            if (
                code == 429
                and attempt < max_attempts - 1
            ):
                time.sleep(retry_delay)
                continue

            raise

    if last_error:
        raise last_error

    raise RuntimeError(
        "Embedding generation failed unexpectedly."
    )


def embed_texts(
    client,
    texts,
):
    return [
        embed_single_text(
            client,
            text,
        )
        for text in texts
    ]


def cosine_similarity(
    vector_a,
    vector_b,
):
    denominator = (
        np.linalg.norm(vector_a)
        * np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(
            vector_a,
            vector_b,
        )
        / denominator
    )


def build_index(api_key):
    if not api_key:
        raise ValueError(
            "Gemini API key is missing."
        )

    client = genai.Client(
        api_key=api_key
    )

    chunks = build_chunks()

    embeddings = embed_texts(
        client,
        [
            chunk["text"]
            for chunk in chunks
        ],
    )

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Chunk and embedding counts do not match."
        )

    return (
        client,
        chunks,
        embeddings,
    )


def retrieve(
    client,
    chunks,
    embeddings,
    question,
    top_k=4,
):
    question = question.strip()

    if not question:
        return []

    if not chunks:
        raise ValueError(
            "Retrieval index contains no chunks."
        )

    if not embeddings:
        raise ValueError(
            "Retrieval index contains no embeddings."
        )

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Chunk and embedding counts do not match."
        )

    if top_k <= 0:
        raise ValueError(
            "top_k must be greater than zero."
        )

    question_embedding = embed_single_text(
        client,
        question,
    )

    scored_chunks = []

    for chunk, embedding in zip(
        chunks,
        embeddings,
    ):
        score = cosine_similarity(
            question_embedding,
            embedding,
        )

        scored_chunks.append(
            {
                "source": chunk["source"],
                "text": chunk["text"],
                "score": score,
            }
        )

    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return scored_chunks[
        :min(top_k, len(scored_chunks))
    ]