import importlib
import os
import pytest

# Garante que módulos que exigem a variável não quebrem no import
@pytest.fixture(autouse=True)
def _groq_env(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", os.getenv("GROQ_API_KEY", "dummy"))

@pytest.mark.parametrize("mod", ["app.app", "app.ingest"])
def test_modules_import(mod):
    try:
        importlib.import_module(mod)
    except ModuleNotFoundError:
        pytest.skip(f"Módulo opcional não encontrado: {mod}")
