---
description: Review text for grammar, typos, and readability. Provides suggestions and corrections in a clear, actionable format.
---

## User Input

```text
$ARGUMENTS
```

## Purpose

Review and improve written text by:
- Identifying and correcting grammar errors
- Catching typos and spelling mistakes
- Improving readability and clarity
- Suggesting better word choices and sentence structures
- Maintaining the original author's voice and intent

## Process

1. **Read the Text**: Carefully read the provided text to understand context and intent.

2. **Grammar & Typo Check**: Identify:
   - Grammar errors (subject-verb agreement, tense consistency, etc.)
   - Spelling mistakes and typos
   - Punctuation errors
   - Capitalization issues

3. **Readability Analysis**: Assess:
   - Sentence length and complexity
   - Paragraph structure and flow
   - Word choice (clarity, precision, conciseness)
   - Active vs passive voice usage
   - Transitions between ideas

4. **Provide Feedback**: Present findings in this format:

   **Grammar & Typos:**
   - List each error with the corrected version
   - Use format: `Original: "..." → Corrected: "..."`

   **Readability Improvements:**
   - Highlight sentences or phrases that could be clearer
   - Suggest specific improvements
   - Explain why the change improves readability

   **Revised Text:**
   - Provide a fully corrected version with all improvements applied
   - Preserve the author's voice and style
   - Maintain the original meaning and intent

5. **Additional Notes**:
   - If the text is already well-written, say so
   - Point out particularly effective passages
   - Offer style suggestions only when they significantly improve clarity

## Guidelines

- Be respectful and constructive
- Focus on substance over style preferences
- Preserve the author's unique voice
- Prioritize clarity and correctness
- Consider the intended audience and purpose
- Don't over-edit - some informal writing styles are intentional

## Example Usage

User provides text:
```
/review-text The quick brown fox jump over the lazy dogs. This is a common typing excersise that people uses for testing keyboards because it contain all letters of the alphabet.
```

Expected response format:
```
**Grammar & Typos:**
- "fox jump" → "fox jumps" (subject-verb agreement)
- "excersise" → "exercise" (spelling)
- "people uses" → "people use" (subject-verb agreement)
- "it contain" → "it contains" (subject-verb agreement)

**Readability Improvements:**
- Consider adding "of the English" before "alphabet" for clarity
- The two sentences could flow better with a connecting word

**Revised Text:**
"The quick brown fox jumps over the lazy dogs. This is a common typing exercise that people use for testing keyboards because it contains all letters of the English alphabet."

**Overall Assessment:**
The text is clear and informative. The corrections mainly address basic grammar consistency.
```
