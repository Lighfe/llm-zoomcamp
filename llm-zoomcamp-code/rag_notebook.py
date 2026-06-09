import marimo

__generated_with = "0.23.6"
app = marimo.App()


@app.cell
def _():
    from dotenv import load_dotenv
    load_dotenv()

    from openai import OpenAI
    openai_client = OpenAI()

    from rag_helper import RAGBase
    from ingest import load_faq_data, build_index

    return RAGBase, build_index, load_faq_data, openai_client


@app.cell
def _(RAGBase, build_index, load_faq_data, openai_client):
    documents = load_faq_data()
    index = build_index(documents)

    assistant = RAGBase(index, openai_client)
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
