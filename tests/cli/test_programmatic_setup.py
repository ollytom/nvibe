from __future__ import annotations

import argparse


def _make_args(**overrides: object) -> argparse.Namespace:
    base: dict[str, object] = {
        "initial_prompt": None,
        "prompt": "hello",
        "max_turns": None,
        "max_price": None,
        "enabled_tools": None,
        "output": "text",
        "agent": "default",
        "setup": False,
        "workdir": None,
        "continue_session": False,
        "resume": None,
    }
    base.update(overrides)
    return argparse.Namespace(**base)