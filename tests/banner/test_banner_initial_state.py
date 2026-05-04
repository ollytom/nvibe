from __future__ import annotations

from unittest.mock import Mock

from vibe.cli.textual_ui.widgets.banner.banner import Banner, BannerState, _pluralize
from vibe.core.config import VibeConfig
from vibe.core.config._settings import ModelConfig, ThinkingLevel
from vibe.core.skills.manager import SkillManager


def _make_mock_config(
    active_model: str = "test-model", thinking: ThinkingLevel = "off"
) -> Mock:
    config = Mock(spec=VibeConfig)
    config.active_model = active_model
    config.models = [active_model]
    config.get_active_model.return_value = ModelConfig(
        name=active_model, provider="mistral", alias=active_model, thinking=thinking
    )
    return config


class TestBannerInitialState:
    """Test that Banner properly displays initial state."""

    def test_pluralize(self) -> None:
        """Test pluralization helper."""
        assert _pluralize(0, "model") == "0 models"
        assert _pluralize(1, "model") == "1 model"
        assert _pluralize(2, "model") == "2 models"
        assert _pluralize(0, "skill") == "0 skills"
        assert _pluralize(1, "skill") == "1 skill"
        assert _pluralize(2, "skill") == "2 skills"

    def test_banner_initial_state(self) -> None:
        skill_manager = Mock(spec=SkillManager)
        skill_manager.custom_skills_count = 0

        banner = Banner(config=_make_mock_config(), skill_manager=skill_manager)

        assert banner._initial_state.active_model == "test-model[off]"
        assert banner._initial_state.models_count == 1
        assert banner._initial_state.skills_count == 0

    def test_banner_shows_thinking_level(self) -> None:
        skill_manager = Mock(spec=SkillManager)
        skill_manager.custom_skills_count = 0

        banner = Banner(
            config=_make_mock_config(thinking="max"), skill_manager=skill_manager
        )

        assert banner._initial_state.active_model == "test-model[max]"

    def test_format_meta_counts(self) -> None:
        skill_manager = Mock(spec=SkillManager)
        skill_manager.custom_skills_count = 0

        banner = Banner(config=_make_mock_config(), skill_manager=skill_manager)

        banner.state = BannerState(models_count=2, skills_count=5)
        result = banner._format_meta_counts()
        assert "2 models" in result
        assert "5 skills" in result
