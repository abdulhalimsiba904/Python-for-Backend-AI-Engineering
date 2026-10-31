"""Provider-independent Day 11 contracts, validation and offline behavior."""
from dataclasses import asdict, dataclass
import json
import math
from typing import Protocol


class SummaryError(ValueError):
    """Safe public error; never include document or provider response text."""


class ProviderError(SummaryError):
    """Network, configuration, refusal or service failure."""

    def __init__(self, message: str, *, code: str | None = None):
        super().__init__(message)
        self.code = code


# Only these application-owned messages reach the CLI. Never display raw exceptions.
PROVIDER_FAILURE_MESSAGES = {
    'configuration': 'Provider configuration error: check API key and model environment variables locally.',
    'authentication': 'Provider authentication failed (401): check your API key locally.',
    'permission': 'Provider permission denied (403): check project/model access.',
    'rate_limit': 'Provider rate limit exceeded (429): wait and check account quota/usage.',
    'timeout': 'Provider request timed out; no automatic retry was attempted.',
    'unavailable': 'Provider service unavailable; try later or select --fallback.',
    'connection': 'Provider connection failed; check your network or select --fallback.',
    'not_found': 'Provider model or endpoint not found (404): check configured model support.',
    'request': 'Provider request rejected: check model support and request configuration.',
    'invalid_response': 'Provider returned an invalid, refused or incomplete AI response.',
}


class ValidationError(SummaryError):
    """Output is not acceptable application data."""


@dataclass
class DocumentSummary:
    title: str
    summary: str
    key_points: list[str]
    open_questions: list[str]

    def to_dict(self):
        return asdict(self)


def validate_summary(value: object) -> DocumentSummary:
    # Parsing JSON is only the first gate. Check shape, types and bounds too.
    fields = {'title', 'summary', 'key_points', 'open_questions'}
    if not isinstance(value, dict) or set(value) != fields:
        raise ValidationError('Summary must contain exactly the four required fields.')
    for name, limit in [('title', 200), ('summary', 2000)]:
        item = value[name]
        if not isinstance(item, str) or not item.strip() or len(item) > limit:
            raise ValidationError(f'{name} must be nonblank text within {limit} characters.')
    for name in ['key_points', 'open_questions']:
        items = value[name]
        if not isinstance(items, list) or len(items) > 10:
            raise ValidationError(f'{name} must be a list of at most 10 strings.')
        if name == 'key_points' and not items:
            raise ValidationError('key_points must contain at least one item.')
        if any(not isinstance(x, str) or not x.strip() or len(x) > 500 for x in items):
            raise ValidationError(f'{name} items must be nonblank strings within 500 characters.')
    return DocumentSummary(value['title'].strip(), value['summary'].strip(),
                           [x.strip() for x in value['key_points']],
                           [x.strip() for x in value['open_questions']])


class SummaryProvider(Protocol):
    # Every adapter returns JSON text and honors its own network timeout.
    def summarize(self, document: str, *, timeout: float) -> str: ...


class MockSummaryProvider:
    """Predictable extractive fixture, not an AI semantic summarizer."""
    def summarize(self, document: str, *, timeout: float) -> str:
        lines = [line.strip() for line in document.splitlines() if line.strip()]
        return json.dumps({
            'title': lines[0][:200],
            'summary': ' '.join(lines)[:2000],
            'key_points': [line[:500] for line in (lines[1:] or lines)[:3]],
            'open_questions': [],
        })


@dataclass
class SummaryResult:
    summary: DocumentSummary
    used_fallback: bool = False


def summarize_document(document: str, provider: SummaryProvider | None = None,
                       *, timeout: float = 15.0, fallback: bool = False) -> SummaryResult:
    if not isinstance(document, str) or not document.strip():
        raise SummaryError('Document must be nonblank text.')
    if len(document) > 20000:
        raise SummaryError('Document exceeds the 20000 character limit.')
    if (isinstance(timeout, bool) or not isinstance(timeout, (int, float))
            or not math.isfinite(timeout) or not 0 < timeout <= 120):
        raise SummaryError('Timeout must be finite and greater than 0, at most 120 seconds.')
    provider = provider if provider is not None else MockSummaryProvider()
    try:
        raw = provider.summarize(document, timeout=timeout)
        if not isinstance(raw, str) or len(raw) > 32000:
            raise ValidationError('Provider output must be JSON text within 32000 characters.')
        return SummaryResult(validate_summary(json.loads(raw)))
    except (ProviderError, ValidationError, json.JSONDecodeError, TimeoutError, RecursionError) as error:
        if fallback:
            raw = MockSummaryProvider().summarize(document, timeout=timeout)
            return SummaryResult(validate_summary(json.loads(raw)), used_fallback=True)
        message = 'Summary failed: service unavailable or output invalid.'
        if isinstance(error, ProviderError):
            message = PROVIDER_FAILURE_MESSAGES.get(error.code, message)
        elif isinstance(error, (ValidationError, json.JSONDecodeError, RecursionError)):
            message = 'Summary failed: provider returned invalid summary data.'
        raise SummaryError(message) from None
