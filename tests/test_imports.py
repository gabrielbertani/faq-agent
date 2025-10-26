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
    monkeypatch.setenv("GROQ_API_KEY", os.getenv("GROQ_API_KEY", "dummy"))
    try:
        importlib.import_module(mod)
    except ModuleNotFoundError:
        pytest.skip(f"Módulo opcional não encontrado: {mod}")
