"""Tests for Settings configuration class — defaults, env overrides, and types."""
from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture
def default_settings(monkeypatch):
    """`Settings` as the *code* declares it — isolated from `.env` and the
    process environment.

    `Settings` resolves env vars first, `.env` second, and field defaults last.
    So a test that asserts a documented default while letting those two layers
    through isn't testing the default at all — it's testing whatever the machine
    happens to be configured with. This repo's `.env` sets `PORT=8010` to dodge a
    local port clash, and that alone made `test_default_port_is_8000` fail on
    every checkout for reasons that had nothing to do with the code. `conftest`
    exports `FACETS_DIR` and `DATA_DIR` for the same reason, which is why
    `test_facets_dir_default` used to pass `facets_dir=` by hand — a workaround
    for this exact leak, applied to one field instead of the cause.

    Clearing every field's env var and disabling `.env` fixes it at the source,
    for the whole class.
    """
    from app.config import Settings

    for field in Settings.model_fields:
        monkeypatch.delenv(field.upper(), raising=False)
        monkeypatch.delenv(field, raising=False)

    return Settings(_env_file=None, secret_key="test-key")


class TestSettingsDefaults:
    """Verify every documented default value."""

    def test_default_host_is_localhost(self, default_settings):
        assert default_settings.host == "127.0.0.1"

    def test_default_port_is_8000(self, default_settings):
        assert default_settings.port == 8000

    def test_debug_is_false_by_default(self, default_settings):
        assert default_settings.debug is False

    def test_external_url_is_empty_by_default(self, default_settings):
        assert default_settings.external_url == ""

    def test_algorithm_is_hs256(self, default_settings):
        assert default_settings.algorithm == "HS256"

    def test_mm_token_expire_hours_default(self, default_settings):
        assert default_settings.mm_token_expire_hours == 8

    def test_invite_token_expire_hours_default(self, default_settings):
        assert default_settings.invite_token_expire_hours == 24

    def test_facets_dir_default(self, default_settings):
        assert default_settings.facets_dir == Path("facets")

    def test_roll_rate_limit_default(self, default_settings):
        assert default_settings.roll_rate_limit == "10/minute"

    def test_auth_rate_limit_default(self, default_settings):
        assert default_settings.auth_rate_limit == "5/minute"

    def test_env_var_overrides_the_default(self, monkeypatch):
        """The isolation above must not hide a real regression: with the env var
        present, it still wins over the default. This is what makes PORT=8010
        work in the first place."""
        from app.config import Settings

        monkeypatch.setenv("PORT", "8010")
        assert Settings(_env_file=None, secret_key="test-key").port == 8010


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
