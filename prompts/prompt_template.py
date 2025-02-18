human_prompt_v1 = """
Input:
- Câu hỏi (Question): The user's query that needs to be answered.
- Context: A text excerpt or dataset providing information related to the question.
Question: {question}.
Context: {context}.

Response Instructions:

Step 1: Read and Understand the Question
- Identify the main requirements of the question.
- Recognize key terms and objectives that need to be addressed.

Step 2: Analyze the Context
- Carefully read the provided context.
- Extract key details, data, and important information related to the keywords in the question.
- Determine which pieces of information are valuable for answering the question.

Step 3: Citation and Reference Rules
    IMPORTANT: Follow these citation rules strictly:
    When metadata is available:
    ✅ DO: Cite using the metadata format provided
    Example: "According to Smith et al. (2023)..." or "Research by Harvard Medical School (2024) shows..."
    ❌ DO NOT: Use phrases like "according to the context" or "cited by context"
    When quoting:
    ✅ DO: Use the exact citation format provided in the quotes
    ❌ DO NOT: Modify or simplify the citation format
    When no metadata is available:
    Present the information without citation phrases
    Focus on the factual content itself
    
Step 4: Use the RAG Mechanism (Retrieval Augmentation)
- If the context is missing some details or requires additional information, initiate a retrieval process to fetch extra data from external sources (if the system supports it).
- Combine the additional information with the existing context.

Step 5: Construct the Answer
- Organize the relevant information in a logical and coherent order.
- Draft a comprehensive answer, detailing each step.
- Ensure that the answer accurately reflects the extracted information and closely aligns with the question.

Step 6: Verify and Validate
- Reassess the accuracy and completeness of the information used.
- Check for any conflicting or missing details.
- If necessary, supplement or adjust the answer accordingly.

Step 7: Present the Final Answer
- Ensure that the final answer is clear, understandable, and logically structured.
- Provide explanations for each reasoning step (if needed) to help the user understand the process.
- **Important:** When presenting the answer, do not state that it is based solely on the context; if metadata of the context is available, indicate that the answer is based on the metadata of the context (nếu có).

Step 8: Handle Cases Where the Question Cannot Be Answered
- If, after all the above steps, the system is unable to provide a suitable answer, respond with:
  "Tôi xin lỗi, không thể trả lời được câu hỏi."

-----------------------------------------------
Example:

Question: “Làm thế nào để bảo quản thực phẩm hiệu quả trong tủ lạnh?”  
(How to effectively preserve food in the refrigerator?)

Context: A text description detailing appropriate temperatures, preservation times for different types of food, and tips for food arrangement. 

Answer Process:
1. Read and understand the question regarding food preservation methods.
2. Extract information on temperature, preservation times, and arrangement tips from the context.
3. Link the extracted information to the specific requirements of the question, relying on the metadata if available.
4. If the context lacks sufficient detail, use the retrieval mechanism to fetch additional data on preservation methods.
5. Draft a detailed answer, listing the preservation steps in order from adjusting temperature, arranging food, to storage duration.
6. Verify the accuracy of the provided information.
7. Present the final, coherent, and comprehensive answer, noting that it is based on the metadata of the context (nếu có).
8. If a suitable answer cannot be provided, respond with:
   "Tôi xin lỗi, không thể trả lời được câu hỏi."

Question: "What are the effects of Vitamin C on the immune system?"
Context: "Vitamin C enhances immune system function through multiple mechanisms" (Dr. James Smith, Immunology Review, 2023)
❌ Incorrect Answer:
According to the context, Vitamin C enhances immune system function.
✅ Correct Answer:
According to Dr. James Smith in Immunology Review (2023), Vitamin C enhances immune system function through multiple mechanisms.
Citation Examples

Single Author with Date:
Original: "The study shows..." (Johnson, 2024)
Correct citation: "Johnson (2024) demonstrates that..."

Multiple Authors:

Original: "Research indicates..." (Smith, Chen, & Wilson, 2023)
Correct citation: "Smith et al. (2023) found that..."

Institutional Author:

Original: "Guidelines suggest..." (World Health Organization, 2024)
Correct citation: "The World Health Organization (2024) recommends..."

Direct Quotes:

Original: "Exact text..." (Author, Year, p. 123)
Correct citation: As stated by Author (Year, p. 123), "exact text..."
-----------------------------------------------
"""

human_prompt_v2 = """
# Enhanced Question-Answering Processing Template
Question: {question}.
Context: {context}.
## Input Format
1. Question (Câu hỏi): 
   - The user's query requiring an answer
   - Format: Can be in Vietnamese or English

2. Context:
   - Relevant text excerpt(s) or dataset
   - May include metadata and citations
   - Can contain information in either/both languages

## Language Guidelines
1. Primary Response Language:
   - Match the language of the question
   - If question is bilingual, default to Vietnamese
   - Technical terms should be provided in both languages on first use

2. Citation Language:
   - Maintain original language of the source
   - Provide translation in brackets if different from response language
   - Example: "According to Nguyễn (2023) [Study on Vietnamese Diet]..."
## Processing Steps

### Step 1: Question Analysis
- Identify:
  + Main requirements
  + Key terms
  + Expected output format
  + Required language for response
- Note any specific constraints or parameters

### Step 2: Context Analysis
- Process the provided context:
  + Extract relevant information
  + Identify key data points
  + Note source metadata
  + Mark citation requirements
- Create information hierarchy based on relevance

### Step 3: Citation Management
Follow these rules strictly:

When metadata is available:
```
✅ DO: Use full metadata format
Example: "According to Trần et al. (2023) in the Journal of Vietnamese Studies..."

❌ DO NOT: 
- Use generic phrases like "according to the context"
- Omit available metadata
- Modify citation formats
```

When quoting:
```
✅ DO:
- Use exact text in original language
- Provide translation if needed
- Include page numbers when available

❌ DO NOT:
- Paraphrase direct quotes
- Change citation format
```

When metadata is unavailable:
```
- Present information directly
- Focus on content accuracy
- Avoid reference to source
```

### Step 4: RAG Implementation
For systems with retrieval capabilities:
1. Identify information gaps in context
2. Specify retrieval parameters:
   - Relevance criteria
   - Time constraints
   - Language preferences
3. Integration rules:
   - Mark retrieved vs. context information
   - Validate source compatibility
   - Maintain citation standards

### Step 5: Answer Construction
1. Organization:
   - Logical flow
   - Clear hierarchy
   - Progressive detail

2. Structure:
   ```
   - Summary (2-3 sentences)
   - Main explanation
   - Supporting evidence
   - Additional considerations
   - Sources (if applicable)
   ```

3. Quality checks:
   - Information accuracy
   - Citation completeness
   - Language consistency
   - Logical coherence

### Step 6: Verification Process
Systematic check of:
1. Answer completeness
2. Citation accuracy
3. Language consistency
4. Source reliability
5. Logical flow
6. Technical accuracy

### Step 7: Response Formatting
Standard format:
```markdown
[Summary]
Brief overview of answer (2-3 sentences)

[Main Response]
Detailed explanation with proper citations

[Supporting Evidence]
Additional data and examples

[Sources]
Complete citation list (if applicable)
```

### Step 8: Error Handling
If unable to provide appropriate answer:
- Vietnamese: "Tôi xin lỗi, không thể trả lời được câu hỏi vì [lý do cụ thể]."
- English: "I apologize, but I cannot answer this question because [specific reason]."

## Example Implementation

Question: "What are the health benefits of green tea?"
Context: "Green tea contains polyphenols that support immune function (Dr. Lê Văn Minh, Vietnam Journal of Nutrition, 2023)"

✅ Correct Response Format:
```markdown
[Summary]
Green tea offers several evidence-based health benefits, primarily due to its polyphenol content.

[Main Response]
According to Dr. Lê Văn Minh in the Vietnam Journal of Nutrition (2023), green tea contains polyphenols that support immune function. 

[Supporting Evidence]
- Clinical research details
- Specific benefits
- Usage recommendations

[Sources]
Lê, V.M. (2023). Polyphenol Content Analysis in Vietnamese Green Tea. Vietnam Journal of Nutrition, 15(2), 45-52.
```

## Quality Assurance Checklist
- [ ] Language consistency maintained
- [ ] Citations properly formatted
- [ ] Information accurately represented
- [ ] Logical flow achieved
- [ ] Sources properly credited
- [ ] Translations provided where necessary

## Note on Updates
This template should be reviewed and updated based on:
1. User feedback
2. Error patterns
3. New requirements
4. Performance metrics
"""