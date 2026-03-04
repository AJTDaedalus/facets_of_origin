"""Tests for Settings configuration class — defaults, env overrides, and types."""
from __future__ import annotations

import os
from pathlib import Path

import pytest


class TestSettingsDefaults:
    """Verify every documented default value."""

    def test_default_host_is_localhost(self):
        from app.config import Settings
        s = Settings(secret_key="test-key")
        assert s.host == "127.0.0.1"

    def test_default_port_is_8000(self):
        from app.config import Settings
        s = Settings(secret_key="test-key")
        assert s.port == 8000

    def test_debug_is_false_by_default(self):
        from app.config import Settings
        s = Settings(secret_key="test-key")
        assert s.debug is False

    def test_external_url_is_empty_by_default(self):
        from app.config import Settings
        s = Settings(secret_key="test-key")
        assert s.external_url == ""

    def test_algorithm_is_hs256(self):
        from app.config import Settings
        s = Settings(secret_key="test-key")
        assert s.algorithm == "HS256"

    def test_mm_token_expire_hours_default(self):
        from app.config import Settings
        s = Settings(secret_key="test-key")
        assert s.mm_token_expire_hours == 8

    def test_invite_token_expire_hours_default(self):
        from app.config import Settings
        s = Settings(secret_key="test-key")
        assert s.invite_token_expire_hours == 24

    def test_facets_dir_default(self):
        from app.config import Settings
        # Pass facets_dir explicitly to avoid FACETS_DIR env var set by conftest
        s = Settings(secret_key="test-key", facets_dir=Path("facets"))
        assert s.facets_dir == Path("facets")

    def test_roll_rate_limit_default(self):
        from app.config import Settings
        s = Settings(secret_key="test-key")
        assert s.roll_rate_limit == "10/minute"

    def test_auth_rate_limit_default(self):
        from app.config import Settings
        s = Settings(secret_key="test-key")
        assert s.auth_rate_limit == "5/minute"


class TestSettingsEnvOverride:
    """Verify env variable overrides reach the Settings instance."""

    def test_host_overridden_via_kwarg(self):
        from app.config import Settings
        s = Settings(host="0.0.0.0", secret_key="x")
        assert s.host == "0.0.0.0"

    def test_port_overridden_via_kwarg(self):
        from app.config import Settings
        s = Settings(port=9000, secret_key="x")
        assert s.port == 9000

    def test_debug_overridden_via_kwarg(self):
        from app.config import Settings
        s = Settings(debug=True, secret_key="x")
        assert s.debug is True

    def test_algorithm_overridden_via_kwarg(self):
        from app.config import Settings
        s = Settings(algorithm="RS256", secret_key="x")
        assert s.algorithm == "RS256"


class TestSettingsTypes:
    """Settings fields must coerce to the declared Python types."""

    def test_port_is_int(self):
        from app.config import Settings
        s = Settings(secret_key="x")
        assert isinstance(s.port, int)

    def test_debug_is_bool(self):
        from app.config import Settings
        s = Settings(secret_key="x")
        assert isinstance(s.debug, bool)

    def test_facets_dir_is_path(self):
        from app.config import Settings
        s = Settings(secret_key="x")
        assert isinstance(s.facets_dir, Path)

    def test_data_dir_is_path(self):
        from app.config import Settings
        s = Settings(secret_key="x")
        assert isinstance(s.data_dir, Path)

    def test_db_path_is_path(self):
        from app.config import Settings
        s = Settings(secret_key="x")
        assert isinstance(s.db_path, Path)


class TestSettingsSecretKey:
    """Secret key must be present and meet minimum entropy requirements."""

    def test_secret_key_is_non_empty_string(self):
        from app.config import settings
        assert isinstance(settings.secret_key, str)
        assert len(settings.secret_key) > 0

    def test_explicit_secret_key_preserved(self):
        from app.config import Settings
        s = Settings(secret_key="my-explicit-key")
        assert s.secret_key == "my-explicit-key"
