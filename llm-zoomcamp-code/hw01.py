import marimo

__generated_with = "0.23.6"
app = marimo.App()


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

    files = reader.read()
    return (files,)


@app.cell
def _(files):
    documents = []

    for file in files:
        _doc = file.parse()
        documents.append(_doc)
    return (documents,)


@app.cell
def _(documents):
    from sqlitesearch import TextSearchIndex

    sqlite_index = TextSearchIndex(
        text_fields=["content"],
        keyword_fields=["filename"],
        db_path="lessons.db"
    )

    for _doc in documents:
        sqlite_index.add(_doc)
        print(f"""Added: {_doc["content"][:60]}...""")

    sqlite_index.close()
    print("Done. Index saved to lessons.db")
    return


@app.cell
def _():
    from minsearch import Index

    return (Index,)


@app.cell
def _(Index):
    def build_index(documents):
        index = Index(
            text_fields=["content"],
            keyword_fields=["filename"]
        )
        index.fit(documents)
        return index

    return (build_index,)


@app.cell
def _(build_index, documents):
    index = build_index(documents)
    return (index,)


@app.cell
def _():
    q_2 = "How does the agentic loop keep calling the model until it stops?"
    return (q_2,)


@app.cell
def _():
    from dotenv import load_dotenv
    load_dotenv()

    from openai import OpenAI
    openai_client = OpenAI()

    from rag_helper import CustomRAG

    return CustomRAG, openai_client


@app.cell
def _(CustomRAG, index, openai_client):
    assistant = CustomRAG(index, openai_client)
    return (assistant,)


@app.cell
def _(assistant, q_2):
    assistant.search(q_2)
    return


@app.cell
def _(assistant, q_2):
    assistant.rag(q_2)
    return


@app.cell
def _(assistant):
    response = assistant.last_response
    return (response,)


@app.cell
def _(response):
    response.usage
    return


@app.cell
def _(documents):
    from gitsource import chunk_documents

    chunks = chunk_documents(documents, size=2000, step=1000)
    return (chunks,)


@app.cell
def _(chunks):
    len(chunks)
    return


@app.cell
def _(build_index, chunks):
    chunk_index = build_index(chunks)
    return (chunk_index,)


@app.cell
def _(CustomRAG, chunk_index, openai_client):
    chunk_assistant = CustomRAG(chunk_index, openai_client)
    return (chunk_assistant,)


@app.cell
def _(chunk_assistant, q_2):
    chunk_assistant.rag(q_2)
    chunk_assistant.last_response.usage
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
