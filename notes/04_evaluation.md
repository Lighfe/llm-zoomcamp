# Intro
1. Interact -> logs questions
2. Generate Data from real Answers create new questions
    - A = the original answer in the FAQ
    - Q* = a question generated from that answer by an LLM
    - A' = the answer produced by our RAG system when gien Q*
    - We compare A' with A to see if the system produced the right anwer

We can now  
- compare different search mthods (minsearch vs vector search s hybrid)
- tune parameters (boost values, number of results, prompt templates)
- compare different LLMs
- track improvement over time

# Generating Ground Truth
- load faq data as done previously
- for structured data we use from pydantic BaseModel to create simple Questions class
- 