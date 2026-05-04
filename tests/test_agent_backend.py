from __future__ import annotations

import pytest

from tests.conftest import build_test_agent_loop, build_test_vibe_config
from tests.mock.utils import mock_llm_chunk
from tests.stubs.fake_backend import FakeBackend
from vibe.core.config import ModelConfig, ProviderConfig, VibeConfig
from vibe.core.types import Backend


def _two_model_vibe_config(active_model: str) -> VibeConfig:
    """VibeConfig with two models so we can switch active_model."""
    models = [
        ModelConfig(
            name="mistral-vibe-cli-latest", provider="mistral", alias="devstral-latest"
        ),
        ModelConfig(
            name="devstral-small-latest", provider="mistral", alias="devstral-small"
        ),
    ]
    providers = [
        ProviderConfig(
            name="mistral",
            api_base="https://api.mistral.ai/v1",
            api_key_env_var="MISTRAL_API_KEY",
            backend=Backend.MISTRAL,
        )
    ]
    return build_test_vibe_config(
        active_model=active_model, models=models, providers=providers
    )


@pytest.mark.asyncio
async def test_passes_x_affinity_header_when_asking_an_answer(vibe_config: VibeConfig):
    backend = FakeBackend([mock_llm_chunk(content="Response")])
    agent = build_test_agent_loop(config=vibe_config, backend=backend)

    [_ async for _ in agent.act("Hello")]

    assert len(backend.requests_extra_headers) > 0
    headers = backend.requests_extra_headers[0]
    assert headers is not None
    assert "x-affinity" in headers
    assert headers["x-affinity"] == agent.session_id


@pytest.mark.asyncio
async def test_passes_x_affinity_header_when_asking_an_answer_streaming(
    vibe_config: VibeConfig,
):
    backend = FakeBackend([mock_llm_chunk(content="Response")])
    agent = build_test_agent_loop(
        config=vibe_config, backend=backend, enable_streaming=True
    )

    [_ async for _ in agent.act("Hello")]

    assert len(backend.requests_extra_headers) > 0
    headers = backend.requests_extra_headers[0]
    assert headers is not None
    assert "x-affinity" in headers
    assert headers["x-affinity"] == agent.session_id


@pytest.mark.asyncio
async def test_updates_tokens_stats_based_on_backend_response(vibe_config: VibeConfig):
    chunk = mock_llm_chunk(content="Response", prompt_tokens=100, completion_tokens=50)
    backend = FakeBackend([chunk])
    agent = build_test_agent_loop(config=vibe_config, backend=backend)

    [_ async for _ in agent.act("Hello")]

    assert agent.stats.context_tokens == 150


@pytest.mark.asyncio
async def test_updates_tokens_stats_based_on_backend_response_streaming(
    vibe_config: VibeConfig,
):
    final_chunk = mock_llm_chunk(
        content="Complete", prompt_tokens=200, completion_tokens=75
    )
    backend = FakeBackend([final_chunk])
    agent = build_test_agent_loop(
        config=vibe_config, backend=backend, enable_streaming=True
    )

    [_ async for _ in agent.act("Hello")]

    assert agent.stats.context_tokens == 275
