from tests.conftest import MockLLMProvider


def test_mock_llm_lifecycle():
    llm = MockLLMProvider()
    assert not llm.is_loaded

    llm.load()
    assert llm.is_loaded

    response = llm.generate("test prompt")
    assert len(response.text) > 0
    assert response.tokens_used > 0

    llm.unload()
    assert not llm.is_loaded
