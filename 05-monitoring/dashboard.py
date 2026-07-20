import streamlit as st
from dataclasses import asdict
import pandas as pd
from db_query import get_conversations, get_stats, get_feedback_stats

# Show the summary metrics:
st.title("Course Assistant Dashboard")

stats = get_stats()
feedback_stats = get_feedback_stats()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total conversations", stats.total)
col2.metric("Avg response time", f"{stats.avg_response_time:.2f}s")
col3.metric("Total cost", f"${stats.total_cost:.4f}")
col4.metric("Avg tokens", f"{stats.avg_tokens:.0f}")

col5, col6 = st.columns(2)
col5.metric("👍 Feedback", feedback_stats.thumbs_up)
col6.metric("👎 Feedback", feedback_stats.thumbs_down)

# Charts for cost and response time over time:
records = get_conversations(limit=100)
df = pd.DataFrame([asdict(r) for r in records])

st.subheader("Cost over time")
st.line_chart(df, x="timestamp", y="cost")

st.subheader("Response time over time")
st.line_chart(df, x="timestamp", y="response_time")

# Show the recent conversations:
st.subheader("Recent conversations")
records = get_conversations(limit=5)

for record in records:
    st.write(f"**{record.prompt[:80]}...**")
    st.write(f"{record.answer[:200]}...")
    st.write(f"Time: {record.response_time:.2f}s | Cost: ${record.cost:.4f}")
    st.divider()