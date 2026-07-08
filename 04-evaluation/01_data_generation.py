import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    from ingest import load_faq_data

    return (load_faq_data,)


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
def _(documents):
    doc = documents[0]
    print(doc["id"])
    print(doc["question"])
    print(doc["answer"])
    return (doc,)


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
def _():
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()
    openai_client = OpenAI()
    return (openai_client,)


@app.cell
def _():
    import json

    return (json,)


@app.cell
def _(doc, json):
    user_prompt = json.dumps(doc)
    return (user_prompt,)


@app.cell
def _(data_gen_instructions, user_prompt):
    messages = [
        {"role": "developer", "content": data_gen_instructions},
        {"role": "user", "content": user_prompt}
    ]
    return (messages,)


@app.cell
def _(Questions, messages, openai_client):
    response_1 = openai_client.responses.parse(
        model="gpt-5.4-mini",
        input=messages,
        text_format=Questions
    )
    return (response_1,)


@app.cell
def _(response_1):
    result_1 = response_1.output_parsed
    print(result_1.questions)
    return


@app.cell
def _():
    from evaluation_utils import llm_structured
    from evaluation_utils import calc_price

    return calc_price, llm_structured


@app.cell
def _(
    Questions,
    data_gen_instructions,
    llm_structured,
    openai_client,
    user_prompt,
):
    result_2, usage_2 = llm_structured(
        openai_client,
        data_gen_instructions,
        user_prompt,
        Questions
    )

    print(result_2.questions)
    return result_2, usage_2


@app.cell
def _(usage_2):
    usage_2.input_tokens, usage_2.output_tokens
    return


@app.cell
def _(calc_price, usage_2):
    calc_price(usage_2)
    return


@app.cell
def _(doc, result_2):
    records = []

    for _q in result_2.questions:
        records.append({
            "question": _q,
            "document": doc["id"]
        })

    records
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
