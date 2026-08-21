import os

from pypdf import PdfReader

from rag.vector_store import VectorStore


class RAGTool:

    def __init__(self, documents_path="rag/documents"):

        self.documents_path = documents_path

        self.vector_store = VectorStore()

        self.load_documents()

    # --------------------------------------------------
    # Load documents
    # --------------------------------------------------

    def load_documents(self):

        documents = []

        if not os.path.exists(self.documents_path):

            print(
                f"Documents folder not found: "
                f"{self.documents_path}"
            )

            return

        for filename in os.listdir(self.documents_path):

            file_path = os.path.join(
                self.documents_path,
                filename
            )

            if not os.path.isfile(file_path):
                continue

            # TXT / Markdown
            if filename.lower().endswith((".txt", ".md")):

                text = self.read_text_file(file_path)

            # PDF
            elif filename.lower().endswith(".pdf"):

                text = self.read_pdf_file(file_path)

            else:

                continue

            chunks = self.chunk_text(
                text,
                filename
            )

            documents.extend(chunks)

        self.vector_store.add_documents(
            documents
        )

        print(
            f"Loaded {len(documents)} document chunks."
        )

    # --------------------------------------------------
    # Read text files
    # --------------------------------------------------

    def read_text_file(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    # --------------------------------------------------
    # Read PDF files
    # --------------------------------------------------

    def read_pdf_file(self, file_path):

        text = []

        reader = PdfReader(file_path)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text.append(page_text)

        return "\n".join(text)

    # --------------------------------------------------
    # Create chunks
    # --------------------------------------------------

    def chunk_text(
        self,
        text,
        source,
        chunk_size=500
    ):

        words = text.split()

        chunks = []

        for i in range(
            0,
            len(words),
            chunk_size
        ):

            chunk = " ".join(
                words[i:i + chunk_size]
            )

            if chunk.strip():

                chunks.append({
                    "text": chunk,
                    "source": source
                })

        return chunks

    # --------------------------------------------------
    # Search documents
    # --------------------------------------------------

    def search(
        self,
        query,
        top_k=3
    ):

        results = self.vector_store.search(
            query,
            top_k
        )

        if not results:

            return (
                "No relevant information "
                "found in the documents."
            )

        output = []

        for result in results:

            output.append(
                f"Source: {result['source']}\n"
                f"Similarity: "
                f"{result['score']:.3f}\n"
                f"{result['text']}"
            )

        return "\n\n---\n\n".join(output)