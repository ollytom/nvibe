from __future__ import annotations

from tests.conftest import build_test_vibe_config
from tests.stubs.fake_audio_player import FakeAudioPlayer
from tests.stubs.fake_tts_client import FakeTTSClient
from vibe.cli.narrator_manager import NarratorManager
from vibe.core.tts.tts_client_port import TTSResult


def _make_manager(
    *,
    narrator_enabled: bool = True,
    tts_client: FakeTTSClient | None = None,
) -> tuple[NarratorManager, FakeAudioPlayer]:
    config = build_test_vibe_config(narrator_enabled=narrator_enabled)
    audio_player = FakeAudioPlayer()
    manager = NarratorManager(
        config_getter=lambda: config,
        audio_player=audio_player,
    )
    manager._tts_client = tts_client or FakeTTSClient(
        result=TTSResult(audio_data=b"fake-audio")
    )
    return manager, audio_player
