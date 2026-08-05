import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from google.genai.errors import ClientError, ServerError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception,
    before_sleep_log,
)
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("classifier")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class ClassificationResult(BaseModel):
    """The structured shape we force the LLM to respond in."""

    severity: Literal["critical", "high", "medium", "low"] = Field(
        description=(
            "critical: system-breaking, no workaround, affects many users. "
            "high: major functionality broken, workaround may exist. "
            "medium: minor bug or missing feature, limited impact. "
            "low: cosmetic, typo, or trivial improvement."
        )
    )
    category: Literal["bug", "feature_request", "question", "documentation", "other"] = Field(
        description="What kind of issue this fundamentally is."
    )
    summary: str = Field(
        description="One or two sentence plain-English summary of the issue.",
        max_length=400,
    )


def build_llm() -> ChatGoogleGenerativeAI:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Did you add it to your .env file?"
        )
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        api_key=GEMINI_API_KEY,
        # Note: as of the 3.5/3.6 generation, Google deprecated temperature/
        # top_p/top_k -- the API currently ignores them rather than erroring,
        # but this is no longer doing the "deterministic classification" work
        # it did on 2.5-era models. Left here as documentation of that intent;
        # remove if a future SDK version turns this into a hard error.
        temperature=0,
        timeout=30,  # give up (raise, don't hang) after 30s with no response
    )


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert software engineering triage assistant. "
            "Read the GitHub issue title and body, and classify it strictly "
            "according to the provided schema. Base your judgment only on "
            "the text given — do not assume context that isn't stated.",
        ),
        (
            "human",
            "Issue title: {title}\n\nIssue body:\n{body}",
        ),
    ]
)


def get_classification_chain():
    llm = build_llm()
    structured_llm = llm.with_structured_output(ClassificationResult)
    return PROMPT | structured_llm


# Build once, reused across calls (avoids re-creating the LLM client per issue)
_chain = None


def _get_chain():
    global _chain
    if _chain is None:
        _chain = get_classification_chain()
    return _chain


def _is_retryable(exception: BaseException) -> bool:
    """
    Only retry failures that have a real chance of succeeding on a second try:
      - ServerError (5xx)      -> transient outage on Google's side
      - ClientError, code 429  -> rate limit hit, worth waiting and retrying
      - ValidationError        -> LLM returned something that didn't fit our schema
    Everything else (e.g. 401 bad key, 404 bad model name) fails fast instead
    of burning through retries on something that can never succeed.
    """
    if isinstance(exception, ServerError):
        return True
    if isinstance(exception, ClientError):
        return getattr(exception, "code", None) == 429
    if isinstance(exception, ValidationError):
        return True
    return False


@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    retry=retry_if_exception(_is_retryable),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,  # if all retries exhausted, let the final exception propagate
)
def classify_incident(title: str, body: str | None) -> ClassificationResult:
    """
    Classify a single incident. Retries only on transient failures
    (see _is_retryable). Exponential backoff: 2s, 4s, 8s, then gives up
    (4 attempts total).
    """
    chain = _get_chain()
    result = chain.invoke({"title": title, "body": body or "(no description provided)"})
    return result