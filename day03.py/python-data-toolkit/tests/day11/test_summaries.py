import json
import socket
from types import SimpleNamespace
from urllib.error import HTTPError, URLError
import pytest

from data_toolkit.summaries import (MockSummaryProvider, SummaryError, ProviderError,
    ValidationError, summarize_document, validate_summary)
from data_toolkit.day11_cli import main
from data_toolkit.openai_summary import OpenAISummaryProvider

DOCUMENT = 'Operations Report\nProcessed 120 tickets.\nResponse time improved.'
VALID = {'title': 'Report', 'summary': 'Processed 120 tickets.',
         'key_points': ['120 tickets'], 'open_questions': []}


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    # A regression must fail instead of sending a request or spending money.
    def deny(*args, **kwargs):
        raise AssertionError('Network is forbidden in tests')
    monkeypatch.setattr(socket, 'create_connection', deny)
    monkeypatch.setattr(socket.socket, 'connect', deny)
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    monkeypatch.delenv('OPENAI_MODEL', raising=False)


def test_mock_is_deterministic_and_input_based():
    a = summarize_document(DOCUMENT).summary.to_dict()
    assert a == summarize_document(DOCUMENT).summary.to_dict()
    assert a == {'title': 'Operations Report', 'summary': 'Operations Report Processed 120 tickets. Response time improved.',
                 'key_points': ['Processed 120 tickets.', 'Response time improved.'], 'open_questions': []}
    assert summarize_document('Another title').summary.title == 'Another title'


@pytest.mark.parametrize('value', [None, [], {}, {**VALID, 'extra': 1},
    {**VALID, 'title': ''}, {**VALID, 'summary': True}, {**VALID, 'title': 'x'*201},
    {**VALID, 'summary': 'x'*2001}, {**VALID, 'key_points': 'text'},
    {**VALID, 'key_points': []}, {**VALID, 'key_points': [1]},
    {**VALID, 'open_questions': [None]}, {**VALID, 'open_questions': [' ']},
    {**VALID, 'open_questions': ['x'*501]}, {**VALID, 'key_points': ['x']*11}])
def test_reject_invalid_data(value):
    with pytest.raises(ValidationError):
        validate_summary(value)


@pytest.mark.parametrize('document', ['', '  ', None, 'x'*20001])
def test_input_rejected(document):
    with pytest.raises(SummaryError):
        summarize_document(document)


@pytest.mark.parametrize('timeout', [0, -1, float('nan'), float('inf'), 121, True, '15'])
def test_bad_timeout(timeout):
    with pytest.raises(SummaryError):
        summarize_document(DOCUMENT, timeout=timeout)


@pytest.mark.parametrize('fault', ['{', '{}', 123, 'x'*32001, TimeoutError(), ProviderError('PRIVATE')])
def test_failure_and_explicit_fallback(fault):
    class Broken:
        def summarize(self, document, *, timeout):
            assert timeout == 3
            if isinstance(fault, Exception):
                raise fault
            return fault
    with pytest.raises(SummaryError) as caught:
        summarize_document(DOCUMENT, Broken(), timeout=3)
    assert 'PRIVATE' not in str(caught.value)
    result = summarize_document(DOCUMENT, Broken(), timeout=3, fallback=True)
    assert result.used_fallback
    assert result.summary == summarize_document(DOCUMENT).summary


def test_configuration_fails_before_network():
    with pytest.raises(ProviderError, match='locally'):
        OpenAISummaryProvider().summarize(DOCUMENT, timeout=2)


def test_cli_output_and_errors(tmp_path, capsys):
    path = tmp_path / 'document.txt'
    path.write_text(DOCUMENT, encoding='utf-8')
    assert main([str(path)]) == 0
    assert json.loads(capsys.readouterr().out)['title'] == 'Operations Report'
    assert main([str(path), '--provider', 'groq', '--fallback']) == 0
    result = capsys.readouterr()
    assert 'fallback' in result.err and json.loads(result.out)['key_points']
    assert main([str(path), '--provider', 'groq']) == 1
    result = capsys.readouterr()
    assert result.out == '' and 'Traceback' not in result.err
    assert main([str(tmp_path / 'missing')]) == 1
    capsys.readouterr()
    path.write_bytes(b'\xff')
    assert main([str(path)]) == 1
    assert 'UTF-8' in capsys.readouterr().err


@pytest.mark.parametrize('body', [
    {'status': 'completed', 'output': [{'type': 'message', 'content': [{'type': 'output_text', 'text': json.dumps(VALID)}]}]},
    {'status': 'incomplete', 'output': []}, {'status': 'completed', 'output': []},
    {'status': 'completed', 'output': [{'type': 'message', 'content': [{'type': 'refusal'}]}]},
    [], {'status': 'completed', 'output': None},
])
def test_adapter_responses_without_network(monkeypatch, body):
    import data_toolkit.openai_summary as module
    monkeypatch.setenv('OPENAI_API_KEY', 'test-only-placeholder')
    monkeypatch.setenv('OPENAI_MODEL', 'test-model')
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self, limit): return json.dumps(body).encode()
    def open_request(request, *, timeout):
        assert timeout == 2
        payload = json.loads(request.data)
        assert payload['store'] is False and payload['max_output_tokens'] == 1000
        assert payload['text']['format']['strict'] is True
        return Response()
    monkeypatch.setattr(module, 'build_opener', lambda *args: SimpleNamespace(open=open_request))
    if isinstance(body, dict) and body.get('output') and body['output'][0]['content'][0]['type'] == 'output_text':
        assert summarize_document(DOCUMENT, OpenAISummaryProvider(), timeout=2).summary.title == 'Report'
    else:
        with pytest.raises(ProviderError):
            OpenAISummaryProvider().summarize(DOCUMENT, timeout=2)


@pytest.mark.parametrize('error', [TimeoutError('PRIVATE'), URLError('PRIVATE'),
    HTTPError('https://example.invalid', 401, 'PRIVATE', {}, None),
    HTTPError('https://example.invalid', 429, 'PRIVATE', {}, None),
    HTTPError('https://example.invalid', 500, 'PRIVATE', {}, None)])
def test_adapter_errors_are_safe(monkeypatch, error):
    import data_toolkit.openai_summary as module
    monkeypatch.setenv('OPENAI_API_KEY', 'test-only-placeholder')
    monkeypatch.setenv('OPENAI_MODEL', 'test-model')
    def fail(*args, **kwargs): raise error
    monkeypatch.setattr(module, 'build_opener', lambda *args: SimpleNamespace(open=fail))
    with pytest.raises(ProviderError) as caught:
        OpenAISummaryProvider().summarize(DOCUMENT, timeout=1)
    assert 'PRIVATE' not in str(caught.value)


def test_public_cli_route_offline():
    import os
    from pathlib import Path
    import subprocess
    import sys
    root = Path(__file__).resolve().parents[2]
    env = {**os.environ, 'PYTHONPATH': str(root / 'src')}
    # The default route stays mock; no account configuration is needed.
    result = subprocess.run([sys.executable, '-m', 'data_toolkit.cli',
        'summarize', 'samples/day11_operations.txt'], cwd=root, env=env,
        capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ''
    assert json.loads(result.stdout)['title'] == 'Quarterly Operations Report'


def test_cli_limits_before_provider(tmp_path, capsys):
    path = tmp_path / 'input.txt'
    path.write_text('x' * 20001)
    assert main([str(path), '--provider', 'groq', '--fallback']) == 1
    assert '20000' in capsys.readouterr().err
    path.write_text('Report')
    assert main([str(path), '--timeout', 'nan', '--fallback']) == 1
    assert 'Timeout' in capsys.readouterr().err
