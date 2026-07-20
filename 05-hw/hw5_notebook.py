import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    from starter import index, client
    from rag_helper import RAGBase

    return RAGBase, client, index


@app.cell
def _():
    import sqlite3
    from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult


    class SQLiteSpanExporter(SpanExporter):

        def __init__(self, db_path="traces.db"):
            self.conn = sqlite3.connect(db_path)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS spans (
                    name TEXT,
                    start_time INTEGER,
                    end_time INTEGER,
                    input_tokens INTEGER,
                    output_tokens INTEGER,
                    cost REAL
                )
            """)
            self.conn.commit()

        def export(self, spans):
            for span in spans:
                attrs = dict(span.attributes or {})
                self.conn.execute(
                    "INSERT INTO spans VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        span.name,
                        span.start_time,
                        span.end_time,
                        attrs.get("input_tokens"),
                        attrs.get("output_tokens"),
                        attrs.get("cost"),
                    ),
                )
            self.conn.commit()
            return SpanExportResult.SUCCESS

        def shutdown(self):
            self.conn.close()

        def force_flush(self):
            return True

    return SQLiteSpanExporter, sqlite3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ConsoleSpanExporter, which prints each finished span to the terminal so we can see what OTel captures:
    """)
    return


@app.cell
def _(SQLiteSpanExporter):
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

    provider = TracerProvider()
    provider.add_span_processor(
        SimpleSpanProcessor(SQLiteSpanExporter("traces.db"))
    )
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer("llm-zoomcamp")

    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

    memory_exporter = InMemorySpanExporter()
    provider.add_span_processor(SimpleSpanProcessor(memory_exporter))
    return memory_exporter, tracer


@app.cell
def _(RAGBase, tracer):
    class RAGWithTracing(RAGBase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.tracer = tracer

        def rag(self, query: str) -> str:
            with self.tracer.start_as_current_span("rag"):
                return super().rag(query)

        def search(self, query: str, num_results: int = 5) -> list:
            with self.tracer.start_as_current_span("search"):
                return super().search(query, num_results)
    
        def llm(self, prompt: str):
            with self.tracer.start_as_current_span("llm") as span:
                response = super().llm(prompt)
                usage = response.usage
                span.set_attribute("input_tokens", usage.input_tokens)
                span.set_attribute("output_tokens", usage.output_tokens)
                return response

    return (RAGWithTracing,)


@app.cell
def _(RAGWithTracing, client, index):
    rag_traced = RAGWithTracing(index=index, llm_client=client)
    return (rag_traced,)


@app.cell
def _(rag_traced):
    rag_traced.rag("How does the agentic loop keep calling the model until it stops?")
    return


@app.cell
def _(memory_exporter):
    # deprecated, replaed by the SQLiteSpanExporter

    spans = memory_exporter.get_finished_spans()
    llm_spans = [s for s in spans if s.name == "llm"]
    search_spans = [s for s in spans if s.name == "search"]
    last_llm_span = llm_spans[-1]
    last_search_span = search_spans[-1]

    llm_duration_ms = (last_llm_span.end_time - last_llm_span.start_time) / 1e6
    search_duration_ms = (last_search_span.end_time - last_search_span.start_time) / 1e6

    llm_duration_ms, search_duration_ms

    return


@app.cell
def _(rag_traced):
    rag_traced.rag("Which LLMs are recommended for LLM Zoomcamp?")
    return


@app.cell
def _(sqlite3):
    import pandas as pd

    conn = sqlite3.connect("traces.db")
    df = pd.read_sql_query("SELECT * FROM spans", conn)
    return conn, df, pd


@app.cell
def _(df):
    df["duration_ms"] = df["end_time"] - df["start_time"]
    totals = (
        df[df["name"] != "rag"]
        .groupby("name")["duration_ms"]
        .sum()
    )
    totals
    return


@app.cell
def _(rag_traced):

    for i in range(4):
        rag_traced.rag("How does the agentic loop keep calling the model until it stops?")
    return


@app.cell
def _(conn, pd):
    df_6 = pd.read_sql_query("SELECT * FROM spans", conn)
    df_6 = df_6[df_6["name"] == "llm"]
    df_6.head()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
