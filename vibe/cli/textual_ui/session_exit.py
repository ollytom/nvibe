from __future__ import annotations

from vibe.core.types import AgentStats

def print_session_resume_message(session_id: str | None, stats: AgentStats) -> None:
    if not session_id:
        return

    print(
        "Total tokens used this session: "
        f"input={stats.session_prompt_tokens:,} "
        f"output={stats.session_completion_tokens:,} "
        f"(total={stats.session_total_llm_tokens:,})"
    )
    print("To continue this session, run: vibe --continue")
    print("Or: vibe --resume",  session_id)
