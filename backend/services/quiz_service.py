from __future__ import annotations

import json

from anthropic import AsyncAnthropic

from backend.config import get_settings


QUIZ_PROMPT = """You are a quiz generator expert. Based on the following transcription,
generate {num_questions} multiple choice questions that test understanding of the key concepts.

Rules:
- Each question must have exactly 4 options (A, B, C, D)
- Only one option is correct
- Include a brief explanation for the correct answer
- Questions range from easy to hard
- Focus on practical concepts, not trivial details
- Return ONLY valid JSON - no markdown, no text outside the JSON

Expected schema:
{{
  \"title\": \"string\",
  \"questions\": [
    {{
      \"position\": 1,
      \"question\": \"string\",
      \"option_a\": \"string\",
      \"option_b\": \"string\",
      \"option_c\": \"string\",
      \"option_d\": \"string\",
      \"correct\": \"A\",
      \"explanation\": \"string\"
    }}
  ]
}}

Transcription:
{transcription}"""


class QuizGenerationError(Exception):
    """Raised when the Anthropic service cannot produce valid quiz JSON."""


class QuizService:
    """Generates quizzes from saved transcription content using Anthropic."""

    def __init__(self):
        settings = get_settings()
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is required for quiz generation.")
        self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def generate_from_transcription(self, transcription_content: str, num_questions: int) -> dict:
        prompt = QUIZ_PROMPT.format(num_questions=num_questions, transcription=transcription_content)
        raw = await self._request_json(prompt)

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            retry_raw = await self._request_retry(prompt, raw)
            try:
                return json.loads(retry_raw)
            except json.JSONDecodeError as exc:
                raise QuizGenerationError("Anthropic returned invalid JSON twice.") from exc

    async def _request_json(self, prompt: str) -> str:
        response = await self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()

    async def _request_retry(self, prompt: str, raw: str) -> str:
        response = await self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": raw},
                {
                    "role": "user",
                    "content": "Your response was not valid JSON. Return ONLY the JSON object, nothing else.",
                },
            ],
        )
        return response.content[0].text.strip()