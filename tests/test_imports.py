# tests/test_imports.py
import importlib
import os
import pytest

MODULES = [
    "app.app",
    "app.main",
    "app.ingest",
    "app.logs",
    "app.search_agent",
    "app.search_tools",
]

@pytest.mark.parametrize("mod", MODULES)
def test_imports(mod, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "dummy")
    importlib.import_module(mod)
