import marimo

__generated_with = "0.23.6"
app = marimo.App()


@app.cell
def _():
    from sqlitesearch import TextSearchIndex

    sqlite_index = TextSearchIndex(
        text_fields=["question", "section", "answer"],
        keyword_fields=["course"],
        db_path="faq.db"
    )
    return (sqlite_index,)


@app.cell
def _(sqlite_index):
    sqlite_index.count()
    return


@app.cell
def _():
    from dotenv import load_dotenv
    load_dotenv()

    from openai import OpenAI
    openai_client = OpenAI()

    from rag_helper import RAGBase

    return RAGBase, openai_client


@app.cell
def _(RAGBase, openai_client, sqlite_index):
    assistant = RAGBase(sqlite_index, openai_client)
    return (assistant,)


@app.cell
def _(assistant):
    assistant.rag("I just discovered the course, can I still join?")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
