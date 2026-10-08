"""Strict mode for soul_cradle.authorization: MYTHARA_PRODUCTION=1 (or
strict=True) refuses the ephemeral-key fallback instead of warning."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from soul_cradle.authorization import SoulCradleAuthority, AuthorizationError


def test_default_still_ephemeral_with_warning(monkeypatch, capsys):
    monkeypatch.delenv("SOUL_CRADLE_KEY", raising=False)
    monkeypatch.delenv("MYTHARA_PRODUCTION", raising=False)
    auth = SoulCradleAuthority()
    assert "ephemeral" in capsys.readouterr().out


def test_strict_param_refuses_ephemeral(monkeypatch):
    monkeypatch.delenv("SOUL_CRADLE_KEY", raising=False)
    with pytest.raises(AuthorizationError, match="SOUL_CRADLE_KEY"):
        SoulCradleAuthority(strict=True)


def test_production_env_refuses_ephemeral(monkeypatch):
    monkeypatch.delenv("SOUL_CRADLE_KEY", raising=False)
    monkeypatch.setenv("MYTHARA_PRODUCTION", "1")
    with pytest.raises(AuthorizationError, match="MYTHARA_PRODUCTION"):
        SoulCradleAuthority()


def test_production_env_with_key_works(monkeypatch):
    monkeypatch.setenv("MYTHARA_PRODUCTION", "1")
    monkeypatch.setenv("SOUL_CRADLE_KEY", "a-stable-test-key")
    auth = SoulCradleAuthority()
    payload = {"text": "hi"}
    env = auth.authorize("emit_text", payload, issuer="soul_cradle",
                         purpose="test")
    ok, _reason = auth.verify(env, payload)
    assert ok
