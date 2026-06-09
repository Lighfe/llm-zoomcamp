import marimo

__generated_with = "0.23.6"
app = marimo.App()


@app.cell
def _():
    from ingest import load_faq_data
    documents = load_faq_data()
    return (documents,)


@app.cell
def _(documents):
    docs_llm = [doc for doc in documents if doc['course'] == 'llm-zoomcamp']
    len(docs_llm)
    return (docs_llm,)


@app.cell
def _(docs_llm):
    import time
    from sqlitesearch import TextSearchIndex


    index = TextSearchIndex(
        text_fields=["question", "section", "answer"],
        keyword_fields=["course"],
        db_path="faq.db"
    )

    for doc in docs_llm:
        index.add(doc)
        print(f"""Added: {doc["question"][:60]}...""")
        time.sleep(0.5)

    index.close()
    print("Done. Index saved to faq.db")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
