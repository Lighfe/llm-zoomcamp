import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    import json

    from ingest import load_faq_data
    from evaluation_utils import llm_structured_retry
    from evaluation_utils import calc_price

    return json, llm_structured_retry, load_faq_data


@app.cell
def _():
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()
    openai_client = OpenAI()
    return (openai_client,)


@app.cell
def _(load_faq_data):
    documents = load_faq_data()
    documents_llm = []

    for _doc in documents:
        if _doc["course"] == "llm-zoomcamp":
            documents_llm.append(_doc)

    documents = documents_llm
    len(documents)
    return (documents,)


@app.cell
def _():
    from pydantic import BaseModel

    class Questions(BaseModel):
        questions: list[str]

    return (Questions,)


@app.cell
def _():
    data_gen_instructions = """
    You emulate a student who's taking our course.
    Formulate 5 questions this student might ask based on a FAQ record. The record
    should contain the answer to the questions, and the questions should be complete and not too short.
    If possible, use as fewer words as possible from the record.

    The output should resemble how people ask questions
    on the internet. Not too formal, not too short, not too long.
    """.strip()
    return (data_gen_instructions,)


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
                "document": doc["id"]
            })

        return results, usage

    return (generate_ground_truth,)


@app.cell
def _(documents, generate_ground_truth):
    from tqdm.auto import tqdm

    ground_truth = []
    usages = []

    for doc in tqdm(documents[:5]):
        records, usage = generate_ground_truth(doc)
        ground_truth.extend(records)
        usages.append(usage)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
