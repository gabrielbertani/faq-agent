import asyncio
import types
import importlib

import pytest

import app.app as app


class FakeResult:
    """Async context manager que simula o objeto retornado por agent.run_stream."""
    def __init__(self, chunks):
        self._chunks = chunks

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def stream_output(self, debounce_by=0.01):
        # Simula streaming cumulativo igual ao usado no código (chunk acumulado)
        acc = ""
        for part in self._chunks:
            await asyncio.sleep(0)  # entrega controle ao loop
            acc += part
            yield acc

    def new_messages(self):
        return ["foo", "bar"]


class FakeAgent:
    def __init__(self, chunks=("Hello ", "World")):
        self._chunks = chunks

    def run_stream(self, user_prompt: str):
        # Retorna um context manager async compatível
        return FakeResult(self._chunks)


@pytest.fixture(autouse=True)
def _no_external_io(monkeypatch):
    """Evita IO/prints no teste."""
    # st.write usado no init_agent()
    import streamlit as st
    monkeypatch.setattr(st, "write", lambda *a, **k: None, raising=False)
    # logging para arquivo
    monkeypatch.setattr(app.logs, "log_interaction_to_file", lambda *a, **k: None, raising=False)


def test_stream_response_yields_deltas(monkeypatch):
    agent = FakeAgent(chunks=("Olá ", "mundo", "!"))

    # Consome o generator síncrono que lê da queue
    out = "".join(list(app.stream_response(agent, "hi")))
    assert out == "Olá mundo!"  # texto final acumulado

    # Verifica que salvou resposta completa na sessão
    assert getattr(app.st.session_state, "_last_response", "") == "Olá mundo!"


def test_init_agent_bypassing_cache(monkeypatch):
    """Testa init_agent sem acionar cache do Streamlit nem rede."""
    # Mocks para evitar rede/SDKs
    monkeypatch.setattr(app.ingest, "index_data", lambda owner, repo, filter: {"index": True})
    monkeypatch.setattr(app.search_agent, "init_agent", lambda index, owner, repo: FakeAgent())

    # Usa a função decorada, mas chamando o alvo real com __wrapped__ (bypass do cache)
    agent = app.init_agent.__wrapped__()  # type: ignore[attr-defined]
    assert isinstance(agent, FakeAgent)
