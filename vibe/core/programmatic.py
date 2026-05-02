from __future__ import annotations

import asyncio
from contextlib import aclosing

from pydantic import BaseModel

from vibe import __version__
from vibe.core.agent_loop import AgentLoop
from vibe.core.agents.models import BuiltinAgentName
from vibe.core.config import VibeConfig
from vibe.core.hooks.models import HookConfigResult
from vibe.core.logger import logger
from vibe.core.output_formatters import create_formatter
from vibe.core.types import AssistantEvent, LLMMessage, OutputFormat, Role
from vibe.core.utils import ConversationLimitException

__all__ = ["run_programmatic"]


class ClientMetadata(BaseModel):
    name: str
    version: str


_DEFAULT_CLIENT_METADATA = ClientMetadata(name="vibe_programmatic", version=__version__)


def run_programmatic(
    config: VibeConfig,
    prompt: str,
    max_turns: int | None = None,
    max_price: float | None = None,
    output_format: OutputFormat = OutputFormat.TEXT,
    previous_messages: list[LLMMessage] | None = None,
    agent_name: str = BuiltinAgentName.AUTO_APPROVE,
    client_metadata: ClientMetadata = _DEFAULT_CLIENT_METADATA,
    headless: bool = False,
    hook_config_result: HookConfigResult | None = None,
) -> str | None:
    formatter = create_formatter(output_format)

    agent_loop = AgentLoop(
        config,
        agent_name=agent_name,
        message_observer=formatter.on_message_added,
        max_turns=max_turns,
        max_price=max_price,
        enable_streaming=False,
        headless=headless,
        entrypoint_metadata={
            "agent_entrypoint": "programmatic",
            "agent_version": __version__,
            "client_name": client_metadata.name,
            "client_version": client_metadata.version,
        },
        hook_config_result=hook_config_result,
    )
    logger.info("USER: %s", prompt)

    async def _async_run() -> str | None:
        if previous_messages:
            non_system_messages = [
                msg for msg in previous_messages if not (msg.role == Role.system)
            ]
            agent_loop.messages.extend(non_system_messages)
            logger.info(
                "Loaded %d messages from previous session", len(non_system_messages)
            )

        async with aclosing(agent_loop.act(prompt)) as events:
            async for event in events:
                formatter.on_event(event)
                if isinstance(event, AssistantEvent) and event.stopped_by_middleware:
                    raise ConversationLimitException(event.content)

        return formatter.finalize()

    return asyncio.run(_async_run())
