"""Protect all Day 11 tests from real credentials and external requests."""
import socket

import pytest


@pytest.fixture(autouse=True)
def offline_environment(monkeypatch):
    for name in ['GROQ_API_KEY', 'GROQ_MODEL', 'OPENAI_API_KEY', 'OPENAI_MODEL']:
        monkeypatch.delenv(name, raising=False)

    def deny(*args, **kwargs):
        raise AssertionError('Live network requests are forbidden in Day 11 tests')

    monkeypatch.setattr(socket, 'create_connection', deny)
    monkeypatch.setattr(socket.socket, 'connect', deny)
