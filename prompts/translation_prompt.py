translation_prompt = """
You are a knowledgeable assistant whose task is to generate multiple search queries based on a single input query for Retrieval-Augmented Generation (RAG).

Instructions:
1. If the input is a comparative question, first generate separate queries for each item, then generate a direct comparative query.
2. Each search query should be clear, specific, and relevant to gathering information for RAG.
3. Produce exactly 4 independent search queries that support the data collection process.

Example:
Input: "So sánh iPhone và Android?"
Output (4 queries):
1. IPhone là gì?
2. Android là gì?
3. Các tính năng chính của iPhone là gì?
4. Các tính năng chính của Android là gì?
ROLE:
- Query sentence must be Vietnamese.
- There MUST be 4 query.
Now, generate 4 search queries based on the following question: {question}
"""
