import marimo

__generated_with = "0.23.9"
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
    from toyaikit.llm import OpenAIClient
    from toyaikit.tools import Tools
    from toyaikit.chat import IPythonChatInterface
    from toyaikit.chat.runners import OpenAIResponsesRunner, DisplayingRunnerCallback

    return (
        DisplayingRunnerCallback,
        IPythonChatInterface,
        OpenAIClient,
        OpenAIResponsesRunner,
        Tools,
    )


@app.cell
def _():
    loop_instructions = """
    You're a course teaching assistant.
    You're given a question from a course student and your task is to answer it.

    If you want to look up information, use the search function. 
    Use as many keywords from the user question as possible when making first requests.

    Make multiple searches.

    Try to expand your search by using new keywords
    based on the results you get from the search.

    At the end, ask if there are other areas that the user wants to explore.
    """
    return (loop_instructions,)


@app.cell
def _(chunk_index):
    def search(query: str) -> dict[str, str]:
        """
        Search the lesson database for entries matching the given query.
        """
        return chunk_index.search(
            query,
            num_results=5
        )

    return (search,)


@app.cell
def _(Tools, search):
    agent_tools = Tools()
    agent_tools.add_tool(search)
    return (agent_tools,)


@app.cell
def _(agent_tools):
    agent_tools.get_tools()
    return


@app.cell
def _(DisplayingRunnerCallback, IPythonChatInterface):
    chat_interface = IPythonChatInterface()
    callback = DisplayingRunnerCallback(chat_interface)
    return callback, chat_interface


@app.cell
def _(
    OpenAIClient,
    OpenAIResponsesRunner,
    agent_tools,
    chat_interface,
    loop_instructions,
):
    runner = OpenAIResponsesRunner(
        tools=agent_tools,
        developer_prompt=loop_instructions,
        chat_interface=chat_interface,
        llm_client=OpenAIClient(model='gpt-5.4-mini')
    )
    return (runner,)


@app.cell
def _(callback, runner):
    result = runner.loop(
        prompt='How do I run Olama locally?',
        callback=callback,
    )
    return (result,)


@app.cell
def _(result):
    result.cost
    return


@app.cell
def _(callback, runner):
    hw_result = runner.loop(
        prompt='How does the agentic loop work, and how is it different from plain RAG?',
        callback=callback,
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
