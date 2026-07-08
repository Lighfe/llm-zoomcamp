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
    from gitsource import chunk_documents
    chunks = chunk_documents(documents, size=2000, step=1000)
    return (chunks,)


@app.cell
def _(chunks, embed):
    X = embed.encode_batch([chunk["content"] for chunk in chunks])
    return (X,)


@app.cell
def _():
    from minsearch import VectorSearch

    return (VectorSearch,)


@app.cell
def _(VectorSearch, X, chunks):
    vindex = VectorSearch()
    vindex.fit(X, chunks)
    return (vindex,)


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
def _(build_index, chunks):
    index = build_index(chunks)
    return (index,)


@app.function
def rrf(result_lists, k=60, num_results=5):
    scores = {}
    docs = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"], doc["start"])
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            docs[key] = doc

    ranked = sorted(scores, key=lambda k: scores[k], reverse=True)
    return [docs[key] for key in ranked[:num_results]]


@app.cell
def _(index):
    def text_search(query, num_results=5):
        return index.search(
            query,
            num_results=num_results
        )

    return (text_search,)


@app.cell
def _(embed, vindex):
    def vector_search(query, num_results=5):
        query_vector = embed.encode(query)
        return vindex.search(query_vector, num_results=num_results)

    return (vector_search,)


@app.cell
def _(text_search, vector_search):
    def hybrid_search(query, k=60):
        text_results = text_search(query, num_results=10)
        vector_results = vector_search(query, num_results=10)
        return rrf([text_results, vector_results], k=k)

    return (hybrid_search,)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Continuing with hw4
    """)
    return


@app.cell
def _():
    data_gen_instructions = """
    You emulate a student who is taking our LLM course.
    You are given one lesson page from the course.
    Formulate 5 questions this student might ask that are answered by this page.

    Rules:
    - The page should contain the answer to each question.
    - Make the questions complete and not too short.
    - Use as few words as possible from the page; don't copy its phrasing.
    - The questions should resemble how people actually ask things online:
      not too formal, not too short, not too long.
    - Ask about the content of the lesson, not about its formatting or filename.
    """.strip()
    return (data_gen_instructions,)


@app.cell
def _():
    from pydantic import BaseModel

    class Questions(BaseModel):
        questions: list[str]

    return (Questions,)


@app.cell
def _():
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()
    openai_client = OpenAI()
    return (openai_client,)


@app.cell
def _():
    from evaluation_utils import llm_structured_retry
    import json

    return json, llm_structured_retry


@app.cell
def _(
    Questions,
    data_gen_instructions,
    json,
    llm_structured_retry,
    openai_client,
):
    def generate_ground_truth(doc):
        user_prompt = json.dumps(doc)

        out, usage = llm_structured_retry(
            openai_client,
            data_gen_instructions,
            user_prompt,
            Questions
        )

        results = []

        for q in out.questions:
            results.append({
                "question": q,
                "document": doc["filename"]
            })

        return results, usage

    return (generate_ground_truth,)


@app.cell
def _(documents):
    q1_filenames = {
        "01-agentic-rag/lessons/01-intro.md",
        "01-agentic-rag/lessons/02-environment.md",
        "01-agentic-rag/lessons/03-rag.md",
    }
    q1_docs = [doc for doc in documents if doc["filename"] in q1_filenames]
    return (q1_docs,)


@app.cell
def _(q1_docs):
    q1_docs
    return


@app.cell
def _(generate_ground_truth, q1_docs):
    from tqdm.auto import tqdm

    ground_truth_q1 = []
    usages_q1 = []

    for _doc in tqdm(q1_docs):
        records, usage = generate_ground_truth(_doc)
        ground_truth_q1.extend(records)
        usages_q1.append(usage)
    return tqdm, usages_q1


@app.cell
def _(usages_q1):
    usages_q1
    return


@app.cell
def _():
    import pandas as pd

    df_ground_truth = pd.read_csv("ground-truth.csv")
    ground_truth = df_ground_truth.to_dict(orient="records")
    return df_ground_truth, ground_truth


@app.cell
def _(df_ground_truth):
    df_ground_truth
    return


@app.cell
def _(ground_truth):
    q2 = ground_truth[0]["question"]
    q2
    return (q2,)


@app.cell
def _(q2, text_search):
    r2 = text_search(q2)
    r2
    return (r2,)


@app.cell
def _(q2, r2):
    q2, r2[0]
    return


@app.cell
def _(q2, vector_search):
    r3 = vector_search(q2)
    r3
    return (r3,)


@app.cell
def _(q2, r3):
    q2, r3[0]
    return


@app.function
def compute_relevance(q, search_function):
    doc_id = q["filename"]
    results = search_function(query=q["question"])

    relevance = []
    for d in results:
        relevance.append(int(d["filename"] == doc_id))

    return relevance


@app.cell
def _(tqdm):
    def compute_relevance_total_text(ground_truth, search_function):
        relevance_total = []

        for q in tqdm(ground_truth):
            relevance = compute_relevance(q, search_function)
            relevance_total.append(relevance)

        return relevance_total

    return (compute_relevance_total_text,)


@app.cell
def _(compute_relevance_total_text, ground_truth, text_search):
    relevance_total_text_4 = compute_relevance_total_text(ground_truth, text_search)
    return (relevance_total_text_4,)


@app.function
def hit_rate(relevance):
    cnt = 0

    for line in relevance:
        if 1 in line:
            cnt = cnt + 1

    return cnt / len(relevance)


@app.cell
def _(relevance_total_text_4):
    hit_rate(relevance_total_text_4)
    return


@app.cell
def _(compute_relevance_total_text, ground_truth, vector_search):
    relevance_total_vector_5 = compute_relevance_total_text(ground_truth, vector_search)
    hit_rate(relevance_total_vector_5)
    return (relevance_total_vector_5,)


@app.function
def mrr(relevance):
    total_score = 0.0

    for line in relevance:
        for rank in range(len(line)):
            if line[rank] == 1:
                total_score = total_score + 1 / (rank + 1)
                break

    return total_score / len(relevance)


@app.cell
def _(relevance_total_vector_5):
    mrr(relevance_total_vector_5)
    return


@app.cell
def _(compute_relevance_total_text, ground_truth, hybrid_search):
    hybrid_mrr_by_k = {}

    for _k in [1, 50, 100, 200]:
        _search = lambda query, k=_k: hybrid_search(query, k=k)
        _relevance_total = compute_relevance_total_text(ground_truth, _search)
        hybrid_mrr_by_k[_k] = mrr(_relevance_total)

    hybrid_mrr_by_k
    return (hybrid_mrr_by_k,)


@app.cell
def _(hybrid_mrr_by_k):
    best_k = min(hybrid_mrr_by_k, key=lambda k: (-hybrid_mrr_by_k[k], k))
    best_k
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
