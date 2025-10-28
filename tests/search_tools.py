# tests/test_search_tools.py
from app import search_tools as st
from unittest.mock import patch

def test_build_query():
    assert st.build_query("abc") == "abc*"  # exemplo

@patch("app.search_agent.Client")  # exemplo de mock de SDK
def test_agent_call(mock_client, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "dummy")
    mock_client.return_value.query.return_value = {"ok": True}
    res = st.run_agent("pergunta")
    assert res["ok"] is True
