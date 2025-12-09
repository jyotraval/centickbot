NUTSHELL

- **[DONE !]** Data Gathering: Read and preprocess the data. FAQ retrived

- **[DONE !]** Embedding: Use Sentence-BERT to generate dense vector embeddings for both the document and user queries.
- **[DONE !]** Vector DB: Store document embeddings in a FAISS or Pinecone index for fast retrieval.
User Query: Convert the user’s query into an embedding.
- **[DONE !]** Retrieve Top-k: Use vector search to find the top-k most relevant document chunks.
- **[DONE !]** API: Expose everything via a FastAPI endpoint for easy querying
- **[DONE !]** NLP Generation: Use a model to generate a response, either by concatenating chunks or refining them.

