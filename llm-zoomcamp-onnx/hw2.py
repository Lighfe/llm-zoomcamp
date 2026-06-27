import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    from embedder import Embedder

    embed = Embedder()
    return (embed,)


@app.cell
def _():
    q1 = 'How does approximate nearest neighbor search work?'
    return (q1,)


@app.cell
def _(embed, q1):
    v1 = embed.encode(q1)
    return (v1,)


@app.cell
def _(v1):
    v1[0]
    return


@app.cell
def _():
    from gitsource import GithubRepositoryDataReader

    reader = GithubRepositoryDataReader(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id="8c1834d",
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )

    documents = [file.parse() for file in reader.read()]
    return (documents,)


@app.cell
def _(documents):
    documents[0]
    return


@app.cell
def _(documents):
    content_q2 = next(doc["content"] for doc in documents if doc["filename"] == "02-vector-search/lessons/07-sqlitesearch-vector.md")
    return (content_q2,)


@app.cell
def _(content_q2, embed):
    embed_q2 = embed.encode(content_q2)
    return (embed_q2,)


@app.cell
def _(embed_q2, v1):
    v1.dot(embed_q2)
    return


@app.cell
def _(documents):
    from gitsource import chunk_documents
    chunks = chunk_documents(documents, size=2000, step=1000)
    return (chunks,)


@app.cell
def _(chunks, embed):
    X = embed.encode_batch([chunk["content"] for chunk in chunks])
    return (X,)


@app.cell
def _(X, v1):
    scores = X.dot(v1)
    return (scores,)


@app.cell
def _(scores):
    scores.argmax()
    return


@app.cell
def _(chunks, scores):
    chunks[scores.argmax()]["filename"]
    return


@app.cell
def _():
    from minsearch import VectorSearch

    return (VectorSearch,)


@app.cell
def _():
    from openai import OpenAI
    openai_client = OpenAI()
    return


@app.cell
def _(VectorSearch, X, chunks):
    vindex = VectorSearch()
    vindex.fit(X, chunks) 
    return (vindex,)


@app.cell
def _(embed, vindex):
    q4 = "What metric do we use to evaluate a search engine?"
    v4 = embed.encode(q4)
    results_q4 = vindex.search(v4, num_results=5)
    return (results_q4,)


@app.cell
def _(results_q4):
    results_q4
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
