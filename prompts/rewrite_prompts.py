rewrite_prompt = """Based on the chat history and the latest user question (which may refer to previous exchanges), convert the question into a standalone, clear, and fully informative question. The standalone question should be self-contained, meaning that the reader can understand it even without the chat history.
Note:
- If the current question is already clear and does not require additional context, retain its original form.
- If the question relies on chat history or contains ambiguous references, adjust it to include all necessary context.
- Use precise, clear language and avoid unnecessary ambiguity.
- Do not answer the question; only rephrase it as required.
- The question must be in Vietnamese
Chat History: {context}
Question: {question}
"""
