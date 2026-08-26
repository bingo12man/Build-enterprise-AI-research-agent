import json
import os
from typing import List

from dotenv import load_dotenv
from groq import Groq

from app.models.evidence import EvidenceItem
from app.models.llm import LLMResearchResult
from app.prompts.research_prompt import (
    SYSTEM_PROMPT,
    build_user_prompt,
)
from app.models.exceptions import LLMServiceError
import time
import logging
from app.config.settings import settings


logger = logging.getLogger(
    __name__
)


GROQ_API_KEY = settings.GROQ_API_KEY
GROQ_MODEL = settings.GROQ_MODEL


if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not configured."
    )


if not GROQ_MODEL:
    raise RuntimeError(
        "GROQ_MODEL is not configured."
    )


_client = Groq(
    api_key=GROQ_API_KEY
)


def generate_research_result(
    query: str,
    evidence_items: List[EvidenceItem],
) -> LLMResearchResult:

    if not evidence_items:
        raise ValueError(
            "Cannot generate research result "
            "without evidence."
        )

    user_prompt = build_user_prompt(
        query=query,
        evidence_items=evidence_items,
    )

    schema = LLMResearchResult.schema()

    structured_prompt = (
        user_prompt
        + "\n\nReturn ONLY valid JSON."
        + "\nDo not include markdown."
        + "\nDo not include ```json."
        + "\nDo not include explanations before or after the JSON."
        + "\nThe JSON must match this schema:\n"
        + json.dumps(schema)
    )

    max_attempts = 2

    for attempt in range(
        1,
        max_attempts + 1,
    ):

        try:
            logger.info(
                "Calling LLM | "
                "model=%s | "
                "attempt=%s",
                GROQ_MODEL,
                attempt,
            )

            completion = (
                _client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT,
                        },
                        {
                            "role": "user",
                            "content": structured_prompt,
                        },
                    ],
                    temperature=0,
                )
            )

            content = (
                completion
                .choices[0]
                .message
                .content
            )

            if not content:
                raise LLMServiceError(
                    "LLM returned an empty response."
                )

            cleaned_content = content.strip()

            if cleaned_content.startswith("```json"):
                cleaned_content = cleaned_content[7:]

            elif cleaned_content.startswith("```"):
                cleaned_content = cleaned_content[3:]

            if cleaned_content.endswith("```"):
                cleaned_content = cleaned_content[:-3]

            cleaned_content = (
                cleaned_content.strip()
            )

            parsed_json = json.loads(
                cleaned_content
            )

            return LLMResearchResult(
                **parsed_json
            )

        except LLMServiceError:
            if attempt == max_attempts:
                raise

        except json.JSONDecodeError as error:
            if attempt == max_attempts:
                raise LLMServiceError(
                    "LLM returned invalid JSON."
                ) from error

        except Exception as error:

            logger.exception(
                "LLM request failed | "
                "model=%s | "
                "attempt=%s",
                GROQ_MODEL,
                attempt,
            )

            if attempt == max_attempts:
                raise LLMServiceError(
                    "LLM service request failed."
                ) from error

        time.sleep(1)