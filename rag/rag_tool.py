import os
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np
import pypdf


class SimpleVectorStore:
    """A lightweight in-memory vector store using cosine similarity."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        print(f"Loading embedding model ({model_name})...")
        self.model = SentenceTransformer(model_name)
        self.documents: List[Dict[str, Any]] = []
        self.embeddings: List[np.ndarray] = []

    def add_documents(self, chunks: List[Dict[str, Any]]) -> None:
        """Embeds text chunks and stores them in memory."""
        if not chunks:
            return

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.model.encode(texts, show_progress_bar=False)

        for chunk, emb in zip(chunks, embeddings):
            self.documents.append(chunk)
            norm = np.linalg.norm(emb)
            normalized_emb = emb / norm if norm > 0 else emb
            self.embeddings.append(normalized_emb)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Finds top-K most similar document chunks to a query."""
        if not self.embeddings:
            return []

        query_emb = self.model.encode(query)
        norm = np.linalg.norm(query_emb)
        query_emb = query_emb / norm if norm > 0 else query_emb

        matrix = np.array(self.embeddings)
        scores = np.dot(matrix, query_emb)

        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            doc = self.documents[idx].copy()
            doc["score"] = float(scores[idx])
            results.append(doc)

        return results


class DocumentRAG:
    """RAG tool for parsing local PDFs and text files into a vector store."""

    def __init__(self, docs_dir: str = "rag/documents", chunk_size: int = 500, chunk_overlap: int = 50):
        self.docs_dir = docs_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vector_store = SimpleVectorStore()
        self.load_and_index()

    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text content from a PDF file."""
        text = ""
        try:
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return text

    def _chunk_text(self, text: str, source: str) -> List[Dict[str, Any]]:
        """Splits text into overlapping character chunks."""
        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + self.chunk_size
            chunk_str = text[start:end].strip()

            if chunk_str:
                chunks.append({
                    "text": chunk_str,
                    "source": source,
                    "start": start,
                    "end": end
                })

            start += self.chunk_size - self.chunk_overlap

        return chunks

    def load_and_index(self) -> None:
        """Scan document directory and populate vector store."""
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir, exist_ok=True)
            print(f"Created directory '{self.docs_dir}'. Add PDF or TXT files here.")
            return

        all_chunks = []
        for filename in os.listdir(self.docs_dir):
            file_path = os.path.join(self.docs_dir, filename)

            if filename.endswith(".pdf"):
                text = self._extract_text_from_pdf(file_path)
            elif filename.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            else:
                continue

            if text.strip():
                chunks = self._chunk_text(text, source=filename)
                all_chunks.extend(chunks)

        if all_chunks:
            self.vector_store.add_documents(all_chunks)
            print(f"Loaded {len(all_chunks)} document chunks into vector store.")
        else:
            print("No documents found or indexed.")

    def search(self, query: str, top_k: int = 3) -> str:
        """Search indexed PDF and text document chunks using vector similarity.

        Args:
            query: The text query to search for within indexed documents.
            top_k: Number of relevant document chunks to return.
        """
        results = self.vector_store.search(query=query, top_k=top_k)

        if not results:
            return "No relevant information found in the local documents."

        formatted_results = []
        for res in results:
            formatted_results.append(
                f"Source: {res['source']}\n"
                f"Similarity Score: {res.get('score', 0.0):.3f}\n"
                f"Content: {res['text']}"
            )

        return "\n\n---\n\n".join(formatted_results)