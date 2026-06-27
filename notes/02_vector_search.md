# 01 Intro
- Word2vec
- vector representation of words
- Semantic approach

# 02 Embeddings
- Explains basics of embeddings
- Sentence Transformers (SBERT)
- https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
- Embed sentences and measure similarity
- all-MiniLM-L6-v2
    - 384-dim vector
    - uses cosine similarity (vTw), normalized vectors

# 03 Embeddings dataset
- load again faq data (json format)
- from tqdm.auto import tqdm # to show progressbar
- simple batches via range(0, len(texts), batch_size)

# 04 Vector Search
- matrix vector multiplication
- np.array(vectors)
- X.dot(v1)
- np.argmax, 
- top5 = np.argsort(scores)[-5:][::-1]
- or top5 = np.argsort(-score)[:5]

# 05 Vector Search with minsearch
- from minsearch import VectorSearch
- use "vindex" similar to the index in module 1

# 06 RAG with Vector Search
- Same approach as before:
    1. search
    2. build prompt
    3. send to LLM
- just replace search, and the query needs to be encoded
- can use RAG helper again, overwrite search function
- TODO: investigate how to handle subclasses best

# 07 Vector Sarch with sqlitesearch
- sqllite can be free, (Turso, Render, Liteloft)
- from sqlitesearch import VectorSearchIndex
- store VectorSearchIndex in persistent sqlite db
- we define a new RAGVector class which inherits from RAGBase
- need to encode query with SentenceTransformer

# 08 PGVector
- is extension for postgres that can have vector search
- need to remember to start pgvector
# 09 ONNX Embedder
- more lightweight than sentence-transformers

# Linkedin
- VectorSearch + TextSearch combined with RRF (Reciprocal Rank Fusion)
- Scores from BM25 and dense vector search are on completely different scales and aren't directly comparable
- Elasticsearch - recommend RRF as standard approach for hybrid search
- Databricks Lakebase Search
- RRF sidesteps incompatible score ranges between retrieval systems, requires almost no tuning beyond the rank constant, and naturally promotes diversity in top results.
- https://blog.serghei.pl/posts/reciprocal-rank-fusion-explained/