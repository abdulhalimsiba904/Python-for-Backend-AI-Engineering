"""Groq request/response tests: fake transport only, no API access or credits."""
import io
import json
from http.client import IncompleteRead
from types import SimpleNamespace
from urllib.error import HTTPError, URLError

import pytest

from data_toolkit.day11_cli import main
from data_toolkit.groq_summary import DEFAULT_MODEL, GroqSummaryProvider, NoRedirect
from data_toolkit.summaries import ProviderError, SummaryError, summarize_document

DOCUMENT = 'Operations Report\n120 tickets were processed.'
VALID = {'title': 'Operations Report', 'summary': '120 tickets were processed.',
         'key_points': ['120 tickets processed'], 'open_questions': []}


def envelope(content=None, finish='stop', **message_fields):
    return {'choices': [{'finish_reason': finish, 'message': {
        'role': 'assistant', 'content': json.dumps(VALID) if content is None else content,
        **message_fields}}]}


@pytest.fixture
def transport(monkeypatch):
    import data_toolkit.groq_summary as module
    monkeypatch.setenv('GROQ_API_KEY', 'nonfunctional-test-placeholder')
    state = SimpleNamespace(body=envelope(), error=None, requests=[], raw=None, closed=False)

    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): state.closed = True
        def read(self, size):
            assert size == 128001
            return state.raw if state.raw is not None else json.dumps(state.body).encode()

    def open_request(request, *, timeout):
        state.requests.append((request, timeout))
        if state.error is not None:
            raise state.error
        return Response()

    monkeypatch.setattr(module, 'build_opener', lambda *args: SimpleNamespace(open=open_request))
    return state


def test_supported_request_and_validated_result(transport):
    result = summarize_document(DOCUMENT, GroqSummaryProvider(), timeout=4)
    assert result.summary.to_dict() == VALID and not result.used_fallback
    request, timeout = transport.requests[0]
    assert request.full_url == 'https://api.groq.com/openai/v1/chat/completions'
    assert request.method == 'POST' and timeout == 4
    assert request.get_header('Authorization') == 'Bearer nonfunctional-test-placeholder'
    assert request.get_header('Content-type') == 'application/json'
    assert request.get_header('User-agent') == 'PythonDataToolkit/1.0'
    payload = json.loads(request.data)
    assert payload['model'] == DEFAULT_MODEL == 'openai/gpt-oss-20b'
    assert payload['messages'][0]['role'] == 'system'
    assert payload['messages'][1] == {'role': 'user', 'content': DOCUMENT}
    assert payload['max_completion_tokens'] == 2048
    assert payload['stream'] is False
    schema = payload['response_format']['json_schema']
    assert schema['strict'] is True
    assert schema['schema']['additionalProperties'] is False
    assert set(schema['schema']['required']) == set(VALID)
    assert transport.closed and len(transport.requests) == 1


def test_model_override(monkeypatch, transport):
    monkeypatch.setenv('GROQ_MODEL', 'openai/gpt-oss-120b')
    GroqSummaryProvider().summarize(DOCUMENT, timeout=2)
    assert json.loads(transport.requests[0][0].data)['model'] == 'openai/gpt-oss-120b'


def test_only_groq_key_is_accepted(monkeypatch, transport):
    monkeypatch.delenv('GROQ_API_KEY')
    monkeypatch.setenv('OPENAI_API_KEY', 'nonfunctional-other-provider-placeholder')
    with pytest.raises(SummaryError, match='configuration'):
        summarize_document(DOCUMENT, GroqSummaryProvider())
    assert transport.requests == []


@pytest.mark.parametrize('key', ['', ' ', 'invalid\nheader', 'invalid key', '\u00e9'])
def test_invalid_key_configuration(monkeypatch, transport, key):
    monkeypatch.setenv('GROQ_API_KEY', key)
    with pytest.raises(SummaryError, match='configuration'):
        summarize_document(DOCUMENT, GroqSummaryProvider())
    assert not transport.requests


@pytest.mark.parametrize('timeout', [0, -1, float('nan'), float('inf'), True, 121])
def test_adapter_timeout_validation(transport, timeout):
    with pytest.raises(ProviderError):
        GroqSummaryProvider().summarize(DOCUMENT, timeout=timeout)
    assert not transport.requests


@pytest.mark.parametrize('status, phrase', [
    (400, 'request rejected'), (401, 'authentication'), (403, 'permission'),
    (404, 'model or endpoint'), (408, 'timed out'), (422, 'request rejected'),
    (429, 'rate limit'), (498, 'unavailable'), (500, 'unavailable'),
    (502, 'unavailable'), (503, 'unavailable'), (302, 'request rejected')])
def test_http_failures_are_safe_and_not_retried(transport, status, phrase):
    body = io.BytesIO(b'PRIVATE-DOCUMENT-AND-KEY')
    transport.error = HTTPError('https://api.groq.com', status, 'PRIVATE', {}, body)
    with pytest.raises(SummaryError, match=phrase) as caught:
        summarize_document(DOCUMENT, GroqSummaryProvider())
    assert 'PRIVATE' not in str(caught.value)
    assert len(transport.requests) == 1 and body.closed


@pytest.mark.parametrize('error, phrase', [
    (TimeoutError('PRIVATE'), 'timed out'),
    (URLError(TimeoutError('PRIVATE')), 'timed out'),
    (URLError('PRIVATE'), 'connection'), (OSError('PRIVATE'), 'connection'),
    (IncompleteRead(b'PRIVATE'), 'connection')])
def test_transport_failures(transport, error, phrase):
    transport.error = error
    with pytest.raises(SummaryError, match=phrase) as caught:
        summarize_document(DOCUMENT, GroqSummaryProvider())
    assert 'PRIVATE' not in str(caught.value) and len(transport.requests) == 1


@pytest.mark.parametrize('body', [
    None, [], {}, {'choices': []}, {'choices': None}, {'choices': [None]},
    {'choices': [{'message': None, 'finish_reason': 'stop'}]},
    envelope(finish='length'), envelope(finish='content_filter'),
    envelope(refusal='PRIVATE'), envelope(content=''), envelope(content=123),
    envelope(content='{'), envelope(content='{}'), envelope(content='[]'),
    envelope(content=json.dumps({**VALID, 'title': 123})),
    envelope(content=json.dumps({**VALID, 'key_points': []})),
    envelope(content=json.dumps({**VALID, 'extra': True})),
    envelope(content='x'*32001),
])
def test_invalid_responses_reject_or_fallback(transport, body):
    transport.body = body
    with pytest.raises(SummaryError, match='invalid'):
        summarize_document(DOCUMENT, GroqSummaryProvider())
    result = summarize_document(DOCUMENT, GroqSummaryProvider(), fallback=True)
    assert result.used_fallback and result.summary == summarize_document(DOCUMENT).summary


@pytest.mark.parametrize('raw', [b'{', b'\xff', b'x'*128001, b'['*2000])
def test_bad_bounded_http_body(transport, raw):
    transport.raw = raw
    with pytest.raises(SummaryError, match='invalid'):
        summarize_document(DOCUMENT, GroqSummaryProvider())


def test_cli_error_and_explicit_fallback(tmp_path, capsys, transport):
    path = tmp_path/'input.txt'
    path.write_text(DOCUMENT)
    transport.error = HTTPError('https://api.groq.com', 429, 'PRIVATE', {}, None)
    assert main([str(path), '--provider', 'groq', '--timeout', '3']) == 1
    result = capsys.readouterr()
    assert result.out == '' and 'rate limit' in result.err and 'PRIVATE' not in result.err
    assert main([str(path), '--provider', 'groq', '--fallback']) == 0
    result = capsys.readouterr()
    assert json.loads(result.out)['title'] == 'Operations Report'
    assert 'fallback' in result.err


def test_cli_mock_stays_offline_with_key_present(tmp_path, capsys, transport):
    path = tmp_path/'input.txt'
    path.write_text(DOCUMENT)
    assert main([str(path)]) == 0
    assert json.loads(capsys.readouterr().out)['title'] == 'Operations Report'
    assert not transport.requests


def test_redirects_are_rejected():
    assert NoRedirect().redirect_request(None, None, 302, '', {}, 'https://other.invalid') is None
