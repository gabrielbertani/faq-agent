import os

def test_env_present_or_dummy():
    # Smoke test simples para validar env necessária ao app
    assert os.getenv("GROQ_API_KEY") is not None
