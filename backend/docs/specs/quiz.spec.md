# Quiz Generation Spec

## Objective
Generate multiple-choice questions from a saved transcription using Anthropic
and persist the quiz plus questions in PostgreSQL.

## Contract
POST /quiz/generate
{ "transcription_id": "uuid", "num_questions": 5 }

Response: full quiz object with all questions.

## Business Rules
- Fetch transcription content from the database by ID.
- Call Anthropic with a structured JSON prompt.
- Retry once when JSON parsing fails.
- Save quiz and questions atomically in one transaction.
- num_questions minimum is 3 and maximum is 15.

## Edge Cases
- transcription_id not found -> 404.
- Anthropic returns invalid JSON twice -> 502.
- num_questions out of range -> 422.