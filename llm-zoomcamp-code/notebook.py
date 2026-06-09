import marimo

__generated_with = "0.23.6"
app = marimo.App()


@app.cell
def _():
    from dotenv import load_dotenv
    load_dotenv()
    return


@app.cell
def _():
    from openai import OpenAI
    openai_client = OpenAI()
    return (openai_client,)


@app.cell
def _(openai_client):
    def first_llm(prompt):
        response = openai_client.responses.create(
            model="gpt-5.4-mini",
            input=prompt
        )
        return response.output_text

    return (first_llm,)


@app.cell
def _(first_llm):
    question = 'I just discovered the course. Can I join now?'
    answer = first_llm(question)
    print(answer)
    return (question,)


@app.cell
def _():
    manual_context = """
    I just discovered the course. Can I still join?
    Yes, but if you want to receive a certificate, you need to submit your project while we're still accepting submissions.

    Course: I have registered for the LLM Zoomcamp. When can I expect to receive the confirmation email?
    You don't need it. You're accepted. You can also just start learning and submitting homework (while the form is open) without registering. It is not checked against any registered list. Registration is just to gauge interest before the start date.

    What is the video/zoom link to the stream for the "Office Hours" or live/workshop sessions?
    The zoom link is only published to instructors/presenters/TAs. Students participate via YouTube Live and submit questions to Slido.

    Cloud alternatives with GPU
    Check the quota and reset cycle carefully. Potential options include Google Colab, Kaggle, Databricks.
    """
    return (manual_context,)


@app.cell
def _(manual_context, question):
    manual_prompt = f"""
    Your task is to answer questions from the course participants
    based on the provided context.

    Use the context to find relevant information and provide accurate
    answers. If the answer is not found in the context,
    respond with "I don't know."

    Question:
    {question}

    Context:
    {manual_context}
    """
    return (manual_prompt,)


@app.cell
def _(first_llm, manual_prompt):
    answer_with_context = first_llm(manual_prompt)
    print(answer_with_context)
    return


@app.cell
def _():
    import requests

    docs_url = "https://datatalks.club/faq/json/courses.json"
    docs_response = requests.get(docs_url)
    courses_raw = docs_response.json()
    return courses_raw, requests


@app.cell
def _(courses_raw):
    courses_raw
    return


@app.cell
def _(courses_raw, requests):
    documents = []
    url_prefix = "https://datatalks.club/faq"

    for course in courses_raw:
        course_url = f"""{url_prefix}{course["path"]}"""

        course_response = requests.get(course_url)
        course_response.raise_for_status()
        course_data = course_response.json()

        documents.extend(course_data)

    len(documents)
    return (documents,)


@app.cell
def _(documents):
    # This data comes already perfectly prepared for the search engine, so we can just use it as is.
    documents[0]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are different libraries for search:
    - Apache Lucene
    - Elasticsearch
    - Apache Solr
    They are all quite heavy.

    Lightweight library "minsearch" for small search projects.
    """)
    return


@app.cell
def _(documents):
    from minsearch import Index

    index = Index(
        text_fields=['question', 'section', 'answer'],
        keyword_fields=['course']
    )

    index.fit(documents)
    return (index,)


@app.cell
def _(index):
    def search(question, course="llm-zoomcamp"):
        boost_dict={"question": 2.0, "section": 0.5},
        filter_dict={'course': course}

        return index.search(
            question,
            boost_dict=boost_dict,
            filter_dict=filter_dict,
            num_results=5
        )

    return (search,)


@app.cell
def _(question, search):
    search_results = search(question)
    search_results
    return (search_results,)


@app.cell
def _():
    INSTRUCTIONS = '''
    Your task is to answer questions from the course participants
    based on the provided context.

    Use the context to find relevant information and provide accurate
    answers. If the answer is not found in the context,
    respond with "I don't know."
    '''
    return (INSTRUCTIONS,)


@app.cell
def _():
    USER_PROMPT_TEMPLATE = '''
    Question:
    {question}

    Context:
    {context}
    '''
    return (USER_PROMPT_TEMPLATE,)


@app.function
def build_context(search_results):
    lines = []

    for doc in search_results:
        lines.append(doc["section"])
        lines.append("Q: " + doc["question"])
        lines.append("A: " + doc["answer"])
        lines.append("")

    return "\n".join(lines).strip()


@app.cell
def _(USER_PROMPT_TEMPLATE):
    def build_prompt(question, search_results):
        context = build_context(search_results)
        prompt = USER_PROMPT_TEMPLATE.format(
            question=question,
            context=context
        )
        return prompt.strip()

    return (build_prompt,)


@app.cell
def _(build_prompt, question, search_results):
    prompt = build_prompt(question, search_results)
    print(prompt)
    return (prompt,)


@app.cell
def _(INSTRUCTIONS, openai_client, prompt):
    message_history = [
        {"role": "developer", "content": INSTRUCTIONS},
        {"role": "user", "content": prompt}
    ]

    response = openai_client.responses.create(
        model="gpt-5.4-mini",
        input=message_history
    )
    return (response,)


@app.cell
def _(response):
    print(response.output_text)
    return


@app.cell
def _():
    return


@app.cell
def _(response):
    response.usage
    return


@app.cell
def _(response):
    input_price = 0.75 / 1_000_000
    output_price = 4.50 / 1_000_000

    cost = (
        response.usage.input_tokens * input_price +
        response.usage.output_tokens * output_price
    )

    cost
    return


@app.cell
def _(openai_client):
    def llm(instructions, user_prompt, model="gpt-5.4-mini"):
        message_history = [
            {"role": "developer", "content": instructions},
            {"role": "user", "content": user_prompt}
        ]

        response = openai_client.responses.create(
            model=model,
            input=message_history
        )

        return response.output_text

    return (llm,)


@app.cell
def _(INSTRUCTIONS, build_prompt, llm, search):
    def rag(query, model="gpt-5.4-mini"):
        search_results = search(query)
        prompt = build_prompt(query, search_results)
        answer = llm(INSTRUCTIONS, prompt, model=model)
        return answer

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
