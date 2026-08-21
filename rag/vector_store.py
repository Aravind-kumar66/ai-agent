import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.documents = []
        self.embeddings = []

    def add_documents(self, documents):

        if not documents:
            return

        texts = [
            doc["text"] if isinstance(doc, dict) else doc
            for doc in documents
        ]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        for i, document in enumerate(documents):

            if isinstance(document, dict):

                self.documents.append(document)

            else:

                self.documents.append({
                    "text": document,
                    "source": "unknown"
                })

            self.embeddings.append(
                embeddings[i]
            )

    def search(self, query, top_k=3):

        if not self.documents:
            return []

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )[0]

        scores = np.dot(
            np.array(self.embeddings),
            query_embedding
        )

        indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for index in indices:

            results.append({
                "text": self.documents[index]["text"],
                "source": self.documents[index]["source"],
                "score": float(scores[index])
            })

        return results