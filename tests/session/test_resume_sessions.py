from __future__ import annotations

from vibe.core.session.resume_sessions import SHORT_SESSION_ID_LEN, short_session_id


class TestShortSessionId:
    def test_local_shortens_to_first_chars(self) -> None:
        sid = "abcdef1234567890"
        result = short_session_id(sid)
        assert result == sid[:SHORT_SESSION_ID_LEN]
        assert len(result) == SHORT_SESSION_ID_LEN

    def test_returns_full_id_when_shorter_than_limit(self) -> None:
        sid = "abc"
        assert short_session_id(sid) == "abc"

    def test_empty_string(self) -> None:
        assert short_session_id("") == ""
