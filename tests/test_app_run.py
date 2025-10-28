import types
from contextlib import contextmanager
import pytest

import app.app as app


class DummyMsgCtx:
    def __enter__(self):  # permite "with st.chat_message(...)"
        return self
    def __exit__(self, *exc):
        return False
    def markdown(self, *_a, **_k):
        return None


@contextmanager
def dummy_chat_message(_role):
    yield DummyMsgCtx()


@pytest.fixture(autouse=True)
def _mock_streamlit(monkeypatch):
    # Evita side effects e torna a UI "headless"
    monkeypatch.setattr(app.st, "set_page_config", lambda **k: None, raising=False)
    monkeypatch.setattr(app.st, "title", lambda *_a, **_k: None, raising=False)
    monkeypatch.setattr(app.st, "caption", lambda *_a, **_k: None, raising=False)
    monkeypatch.setattr(app.st, "write", lambda *_a, **_k: None, raising=False)
    monkeypatch.setattr(app.st, "write_stream", lambda gen: "".join(list(gen)), raising=False)
    monkeypatch.setattr(app.st, "chat_message", dummy_chat_message, raising=False)

    # session_state simulado
    class _SS(dict):
        pass
    ss = _SS()
    monkeypatch.setattr(app.st, "session_state", ss, raising=False)

    # Mock do agente para não chamar rede
    class FakeResult:
        def __init__(self, chunks):
            self._chunks = chunks
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            return False
        async def stream_output(self, debounce_by=0.01):
            acc = ""
            for part in self._chunks:
                acc += part
                yield acc
        def new_messages(self):
            return ["m1","m2"]

    class FakeAgent:
        def __init__(self, chunks=("Hi ", "there")):
            self._chunks = chunks
        def run_stream(self, user_prompt: str):
            return FakeResult(self._chunks)

    # Bypassa cache e indexação: init_agent devolve FakeAgent
    monkeypatch.setattr(app, "init_agent", lambda: FakeAgent(), raising=True)

    return ss


def test_run_happy_path(monkeypatch):
    # chat_input retorna uma pergunta → percorre o fluxo de chat
    monkeypatch.setattr(app.st, "chat_input", lambda *_a, **_k: "Pergunta?", raising=False)

    # Executa a UI uma vez
    app.run()

    # Verifica que a conversa foi gravada
    msgs = app.st.session_state["messages"]
    assert msgs[0]["role"] == "user" and "Pergunta?" in msgs[0]["content"]
    assert msgs[1]["role"] == "assistant" and "Hi there" in msgs[1]["content"]


def test_run_no_input(monkeypatch):
    # chat_input sem pergunta → só renderiza histórico vazio
    monkeypatch.setattr(app.st, "chat_input", lambda *_a, **_k: None, raising=False)
    app.run()
    assert app.st.session_state.get("messages", []) == []
